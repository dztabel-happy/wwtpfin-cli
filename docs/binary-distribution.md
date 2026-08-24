# Binary distribution

The public npm package contains only the Node launcher, skills, public documentation and examples. It contains no Python core source.

The launcher resolves one optional platform package: `@dztabel/wwtpfin-darwin-arm64`, `@dztabel/wwtpfin-linux-x64`, or `@dztabel/wwtpfin-win32-x64`. Each platform package publishes the complete PyInstaller `onedir` bundle: `wwtp-fin` plus `_internal/`.

For local maintainer smoke testing only, an unpacked Darwin Apple Silicon bundle may be placed in `dist/darwin-arm64/`. `dist/` is ignored and excluded from npm. Release publication must build and publish the matching platform package; it must not publish `dist/` from this repository.
