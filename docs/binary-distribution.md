# Binary distribution

The public npm package contains only the Node launcher, skills, public documentation and examples. It contains no Python core source.

The launcher resolves one optional platform package:

- `@dztabel/wwtpfin-darwin-arm64`
- `@dztabel/wwtpfin-linux-x64`
- `@dztabel/wwtpfin-win32-x64`

Each platform package contains the complete PyInstaller `onedir` bundle: `wwtp-fin` plus `_internal/`. Build metadata is reduced to the package name and version before staging; local source paths and editable-install metadata must not enter the tarball.

## Local release acceptance

Run from this public repository:

```bash
python3 scripts/release_preflight.py \
  --core-repo ../wwtpfin-cli-core
```

The preflight runs core tests, consistency checks, clean wheel installation and benchmark gates, builds the local platform binary, packs the main and platform npm tarballs, installs both in a temporary directory, then runs `build` and `verify-deliverable` through the installed launcher.

## GitHub release

The public workflow requires:

- a private `dztabel-happy/wwtpfin-cli-core` repository;
- a read-only `CORE_DEPLOY_KEY` secret in the public repository;
- an `NPM_TOKEN` secret allowed to publish the four npm packages.

Dispatch `Release platform packages` with an exact `core_ref` and `publish=false` first. The workflow resolves that ref once to an immutable commit, builds all three platform packages and performs packed-install smoke tests. Repeat with `publish=true` only after the dry run succeeds.

The repository-local `dist/` directory is maintainer scratch space. It is ignored and never published.
