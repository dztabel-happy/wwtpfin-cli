#!/usr/bin/env node
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const packageRoot = findPackageRoot();
const binary = findBundledBinary();

if (require.main === module) {
  if (!binary) {
    const packageName = platformPackageName();
    const version = packageVersion();
    console.error("wwtp-fin: platform package is missing.");
    console.error(packageName
      ? `wwtp-fin: expected optional dependency ${packageName} to provide the binary.`
      : `wwtp-fin: unsupported platform ${process.platform}/${process.arch}.`);
    if (packageName) {
      console.error(`wwtp-fin: run \"npm install -g @dztabel/wwtpfin@${version} ${packageName}@${version}\".`);
    }
    process.exit(1);
  }
  const result = spawnSync(binary, process.argv.slice(2), {
    cwd: process.cwd(), env: { ...process.env, PYTHONUTF8: process.env.PYTHONUTF8 || "1" }, stdio: "inherit",
  });
  if (result.error) {
    console.error(`wwtp-fin: failed to start: ${result.error.message}`);
    process.exit(1);
  }
  process.exit(result.status ?? 1);
}

function findPackageRoot() {
  const candidates = [
    path.resolve(__dirname, ".."),
    path.resolve(__dirname, "node_modules", "@dztabel", "wwtpfin"),
    path.resolve(__dirname, "..", "node_modules", "@dztabel", "wwtpfin"),
  ];
  for (const candidate of candidates) {
    try {
      const manifest = JSON.parse(fs.readFileSync(path.join(candidate, "package.json"), "utf8"));
      if (manifest.name === "@dztabel/wwtpfin") return candidate;
    } catch (_) {}
  }
  return path.resolve(__dirname, "..");
}

function findBundledBinary() {
  const platformBinary = findPlatformPackageBinary();
  if (platformBinary) return platformBinary;
  const executable = process.platform === "win32" ? "wwtp-fin.exe" : "wwtp-fin";
  const candidate = path.join(packageRoot, "dist", `${process.platform}-${process.arch}`, executable);
  return isExecutableFile(candidate) ? candidate : null;
}

function findPlatformPackageBinary() {
  const packageName = platformPackageName();
  if (!packageName) return null;
  try {
    const manifest = require.resolve(`${packageName}/package.json`, { paths: [packageRoot] });
    const executable = process.platform === "win32" ? "wwtp-fin.exe" : "wwtp-fin";
    const candidate = path.join(path.dirname(manifest), executable);
    return isExecutableFile(candidate) ? candidate : null;
  } catch (_) {
    return null;
  }
}

function isExecutableFile(candidate) {
  try {
    return fs.statSync(candidate).isFile();
  } catch (_) {
    return false;
  }
}

function platformPackageName(platform = process.platform, arch = process.arch) {
  return {
    "darwin/arm64": "@dztabel/wwtpfin-darwin-arm64",
    "linux/x64": "@dztabel/wwtpfin-linux-x64",
    "win32/x64": "@dztabel/wwtpfin-win32-x64",
  }[`${platform}/${arch}`] || null;
}

function packageVersion() {
  try {
    return JSON.parse(fs.readFileSync(path.join(packageRoot, "package.json"), "utf8")).version || "latest";
  } catch (_) {
    return "latest";
  }
}

module.exports = { platformPackageName };
