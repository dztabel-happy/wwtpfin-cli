import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const publicRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const platforms = ["darwin-arm64", "linux-x64", "win32-x64"];
const readJson = filename => JSON.parse(readFileSync(filename, "utf8"));
const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);
const npmCommand = args => execFileSync("npm", args, {
  encoding: "utf8",
  stdio: ["ignore", "pipe", "pipe"],
  shell: process.platform === "win32",
});

function notFound(error) {
  for (const output of [error.stdout, error.stderr]) {
    try {
      if (JSON.parse(String(output)).error?.code === "E404") return true;
    } catch {}
  }
  return /(?:^|\n)npm (?:ERR!|error) code E404(?:\s|$)/.test(String(error.stderr));
}

// Validate every already-tested archive and every registry version before the
// first write. A failed build never reaches this job; a partial publish can only
// resume with byte-identical tarballs, never freshly repacked replacements.
export function publishPackages({ files, root = publicRoot, dryRun = false, npm = npmCommand, log = console.log }) {
  const main = readJson(path.join(root, "package.json"));
  const expected = platforms.map(platform => readJson(path.join(root, "npm/platform-packages", platform, "package.json")));
  expected.push(main);
  const pins = Object.fromEntries(expected.slice(0, -1).map(pkg => [pkg.name, main.version]));
  const sorted = object => Object.entries(object ?? {}).sort(([a], [b]) => a.localeCompare(b));
  if (!same(sorted(main.optionalDependencies), sorted(pins)) || expected.some(pkg => pkg.version !== main.version)) {
    throw new Error("Release manifests must share one version and exact platform dependency pins");
  }
  if (files.length !== expected.length) throw new Error("Expected exactly three platform tarballs and one main tarball");

  const archives = new Map();
  for (const filename of files) {
    const archive = path.resolve(filename);
    if (!archive.endsWith(".tgz")) throw new Error("Only packed .tgz files may be published");
    const manifest = JSON.parse(execFileSync("tar", ["-xOf", path.basename(archive), "package/package.json"], { cwd: path.dirname(archive), encoding: "utf8" }));
    const wanted = expected.find(pkg => pkg.name === manifest.name);
    if (!wanted || archives.has(manifest.name)) throw new Error(`Unexpected or duplicate package: ${manifest.name}`);
    for (const field of ["version", "os", "cpu", "files", "bin", "optionalDependencies"]) {
      if (!same(manifest[field], wanted[field])) throw new Error(`${manifest.name}: packed ${field} does not match the release manifest`);
    }
    if (manifest.private) throw new Error(`${manifest.name}: package is private`);
    const entries = execFileSync("tar", ["-tzf", path.basename(archive)], { cwd: path.dirname(archive), encoding: "utf8" }).trim().split(/\r?\n/);
    const paths = entries.filter(entry => !entry.endsWith("/"));
    const allowed = wanted.files ?? [];
    for (const entry of paths) {
      const relative = entry.replace(/^package\//, "");
      const metadata = relative === "package.json" || /^(?:readme|licen[sc]e)(?:\.[^/]*)?$/i.test(relative);
      if (!entry.startsWith("package/") || relative.split("/").includes("..") ||
          /(^|\/)__pycache__(\/|$)|\.py[co]$/.test(relative) ||
          (!metadata && !allowed.some(item => relative === item || relative.startsWith(`${item}/`)))) {
        throw new Error(`${manifest.name}: unexpected packed path ${entry}`);
      }
    }
    if (manifest.name !== main.name) {
      const binary = manifest.os[0] === "win32" ? "wwtp-fin.exe" : "wwtp-fin";
      if (!paths.includes(`package/${binary}`) || !paths.some(entry => entry.startsWith("package/_internal/"))) {
        throw new Error(`${manifest.name}: incomplete onedir platform bundle`);
      }
      if (paths.some(entry => entry.endsWith(".py") || entry.endsWith("/direct_url.json"))) {
        throw new Error(`${manifest.name}: platform archive contains source or build metadata`);
      }
    }
    const integrity = `sha512-${createHash("sha512").update(readFileSync(archive)).digest("base64")}`;
    archives.set(manifest.name, { archive, integrity, spec: `${manifest.name}@${manifest.version}` });
  }

  const planned = expected.map(manifest => {
    const packed = archives.get(manifest.name);
    if (!packed) throw new Error(`Missing package: ${manifest.name}`);
    let published;
    try {
      published = JSON.parse(npm(["view", packed.spec, "dist.integrity", "--json"]));
    } catch (error) {
      if (!notFound(error)) throw error;
      return { ...packed, exists: false };
    }
    if (published !== packed.integrity) throw new Error(`${packed.spec} already exists with different integrity; refusing the entire release`);
    return { ...packed, exists: true };
  });

  for (const packed of planned) {
    if (packed.exists) {
      log(`${packed.spec} already exists with matching integrity; skipped`);
      continue;
    }
    const args = ["publish", packed.archive, "--access", "public", "--ignore-scripts"];
    if (dryRun) args.push("--dry-run");
    npm(args);
    log(`${packed.spec}: ${dryRun ? "publish rehearsal passed" : "published"}`);
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  try {
    publishPackages({ files: args.filter(arg => arg !== "--dry-run"), dryRun: args.includes("--dry-run") });
  } catch (error) {
    console.error(error.message);
    // npm errors are captured: report their diagnosis, without dumping private
    // source trees or retaining logs as public workflow artifacts.
    if (error.stderr) console.error(String(error.stderr));
    process.exitCode = 1;
  }
}
