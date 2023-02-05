# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project will adhere
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) after release of
1.0.0 version.

## [FUTURE]

### Changed

### Added

- 🔲 Logging managing system
- 🔲 Tests for packet parsers
- 🔲 Optimize:
  - 🔲 Pass memoryview between threads (verify threadsafety)
- 🔲 Move compression from Connection.recv

## [1.0.0] - FUTURE - first release

### Features

- ✅ Barely working moving system
- ✅ Parsing basic packets for
  1.12.2. [Full list.](/MinecraftConsoleClient/versions/v1_12_2/FEATURES.md)
- 🔲 Support for "Call before packet handle"
- 🔲 Support for "Call after packet handle"
- 🔲 Basic docs
- 🔲 Fully adopted Architecture
- 🔲 Move serverbound into packet

## [0.X.0] - Future before release of 1.0.0

- 🔲 Organize "versions" folder

- 🔲 Moooore logging
- 🔲 Refactor all code but packet handlers - they will be rewritten after
  implementing Packet
- 🔲 Basic docs

## [0.7.0] - Future
- 🔲 Implemented new version.packet

### Changed
- 🔲 TODO PARSER_ADD_THRESHOLD ?


## [0.6.0] - Next
- ✅ Support for "Call before packet handle"
- ✅ Support for "Call after packet handle"
- ✅ Split packet actions to: parse_packet, and react_to_packet
- ✅ Moved to every reaction to packet to some_packet.react()
- ✅ New handling packets system: 
  - some_packet = SomePacket.parse(data)
  - some_packet.react()

### Changed

## [0.5.0] - 2021-09-11

## Changed

-  Refinement of files
-  Converters now return memoryview of leftover of bytes, see
  [memoryviewvs_bytes_slicing.py](https://github.com/Nielotz/python_benchmarks/blob/master/memoryview_vs_bytes_slicing.py)

## [0.4.1] - 2021-08-22

## Added

- Basic performance analyze system

## [0.4.0] - 2021-08-19

### Changed

- Organize project files

### ADDED

- Create Architecture draft

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