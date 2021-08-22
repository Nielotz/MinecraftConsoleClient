# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project will adhere
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) after release of
1.0.0 version.

## [FUTURE]

### Changed

- 🔲 Optimized parsing packet using memoryview

### Added

- 🔲 Logging managing system
- 🔲 Tests for packet parsers

## [1.0.0] - FUTURE - first release

### Features

- ✅ Barely working moving system
- ✅ Parsing basic packets for
  1.12.2. [Full list.](/MinecraftConsoleClient/versions/v1_12_2/FEATURES.md)
- 🔲 Support for "Call before packet handle"
- 🔲 Support for "Call after packet handle"
- 🔲 Basic docs
- 🔲 Implement Architecture

## [0.X.0] - Future before release of 1.0.0

- 🔲 Organize "versions" folder
- 🔲 Refactor all code but packet handlers - they will be rewritten after
  implementing Packet
- 🔲 Basic docs

## [0.5.1] - Future

### Changed

- 🔲 Support for "Call before packet handle"
- 🔲 Support for "Call after packet handle"

## [0.5.0] - Next release

### Added

- 🔲 Split packet actions to: parse_packet, and react_to_packet

## [0.4.1] - Next release

- 🔲 Moooore logging
- 🔲 Performance analyze system

## [0.4.0] - 2021-08-19

### Changed

- ✅ Organize project files

### ADDED

- ✅ Create Architecture draft

## [0.3.0] - 2021-08-04

### Changed

- Handling of block change - now it works with indirect, and direct palette

### Added

- Feature list of 1.12.2 (with blank scheme)
- Extract unsigned long and short to converters.
- More tests to converters
- Fixed block change to 1.12.2, clientbound, play
- Sandbox for testing chunk packet

### Fixed

- Typos in some files

## [0.1.0]

### Added

- This CHANGELOG