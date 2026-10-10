import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { publishPackages } from "./publish_npm_packages.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const platforms = ["darwin-arm64", "linux-x64", "win32-x64"];

function fixture(t, change = () => {}) {
  const temp = mkdtempSync(path.join(os.tmpdir(), "wwtpfin-publish-test-"));
  t.after(() => rmSync(temp, { recursive: true, force: true }));
  const manifests = [...platforms.map(platform => path.join(root, "npm/platform-packages", platform, "package.json")), path.join(root, "package.json")];
  return manifests.map((filename, index) => {
    const manifest = JSON.parse(readFileSync(filename, "utf8"));
    const directory = path.join(temp, String(index));
    const contents = path.join(directory, "package");
    const files = index === 3
      ? { "npm/wwtp-fin.cjs": "// synthetic launcher" }
      : { [index === 2 ? "wwtp-fin.exe" : "wwtp-fin"]: "synthetic binary", "_internal/runtime.json": "{}" };
    change(manifest, files, index);
    files["package.json"] = JSON.stringify(manifest);
    for (const [name, data] of Object.entries(files)) {
      const destination = path.join(contents, name);
      mkdirSync(path.dirname(destination), { recursive: true });
      writeFileSync(destination, data);
    }
    const archive = path.join(temp, `${index}.tgz`);
    execFileSync("tar", ["-czf", path.basename(archive), "-C", path.relative(path.dirname(archive), directory), "package"], { cwd: path.dirname(archive) });
    return archive;
  });
}

function registry(resolve = () => "E404") {
  const calls = [];
  const npm = args => {
    calls.push(args);
    if (args[0] === "publish") return "";
    const value = resolve(args[1]);
    if (value.startsWith("E")) {
      const error = new Error(`npm ${value}`);
      error.stdout = JSON.stringify({ error: { code: value } });
      throw error;
    }
    return JSON.stringify(value);
  };
  return { npm, calls };
}

function run(files, mock, dryRun = false) {
  publishPackages({ files, root, npm: mock.npm, dryRun, log: () => {} });
}

test("missing platform archive prevents registry access and publication", t => {
  const files = fixture(t);
  const mock = registry();
  assert.throws(() => run(files.slice(1), mock), /exactly three platform/);
  assert.equal(mock.calls.length, 0);
});

test("all archives are checked before writes: version, platform, complete bundle, source boundary", async t => {
  for (const [name, change, message] of [
    ["version", manifest => { manifest.version = "0.0.0"; }, /packed version/],
    ["platform", manifest => { manifest.cpu = ["arm64"]; }, /packed cpu/],
    ["bundle", (_, files) => { delete files["_internal/runtime.json"]; }, /incomplete onedir/],
    ["source", (_, files) => { files["_internal/private.py"] = "private source"; }, /contains source/],
  ]) {
    await t.test(name, child => {
      const files = fixture(child, (manifest, entries, index) => { if (index === 2) change(manifest, entries); });
      const mock = registry();
      assert.throws(() => run(files, mock), message);
      assert.equal(mock.calls.length, 0);
    });
  }
});

test("a late registry integrity mismatch blocks the entire release and the rehearsal", t => {
  const files = fixture(t);
  for (const dryRun of [false, true]) {
    const mock = registry(spec => spec.startsWith("@dztabel/wwtpfin@") ? "sha512-different" : "E404");
    assert.throws(() => run(files, mock, dryRun), /different integrity/);
    assert.equal(mock.calls.length, 4);
    assert.ok(mock.calls.every(args => args[0] === "view"));
  }
});

test("only identical existing tarballs are skipped; remaining platforms publish before main", t => {
  const files = fixture(t);
  const integrity = `sha512-${createHash("sha512").update(readFileSync(files[0])).digest("base64")}`;
  const mock = registry(spec => spec.includes("-darwin-arm64@") ? integrity : "E404");
  run(files, mock);
  assert.ok(mock.calls.slice(0, 4).every(args => args[0] === "view"));
  assert.deepEqual(mock.calls.slice(4).map(args => args[1]), files.slice(1));
  assert.ok(mock.calls.slice(4).every(args => args[0] === "publish" && !args.includes("--dry-run")));
});

test("rehearsal validates every registry version and exercises npm publish with dry-run", t => {
  const files = fixture(t);
  const mock = registry();
  run([...files].reverse(), mock, true);
  assert.ok(mock.calls.slice(0, 4).every(args => args[0] === "view"));
  assert.deepEqual(mock.calls.slice(4).map(args => args[1]), files);
  assert.ok(mock.calls.slice(4).every(args => args[0] === "publish" && args.includes("--dry-run")));
});

test("registry failures other than E404 never authorize a publish", t => {
  const files = fixture(t);
  const mock = registry(spec => spec.startsWith("@dztabel/wwtpfin@") ? "E401" : "E404");
  assert.throws(() => run(files, mock), /E401/);
  assert.equal(mock.calls.length, 4);
  assert.ok(mock.calls.every(args => args[0] === "view"));
});
