# 📜 Changelog

All notable changes to this project will be documented in this file.

This project follows:

- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/)

---

## [Unreleased]

### Added

- Support for metronome generation based on target duration (seconds).
- Explicit FPS configuration from the entry point (`main`).

### Changed

- Update beat images for improved visual clarity
- AudioBuilder now produces a fully finalized AudioSegment with deterministic duration.
- Audio post-processing (sample rate, channels) is fully encapsulated in AudioBuilder.
- Composer no longer handles audio technical parameters.

### Refactored

- Clear separation of responsibilities between Composer, AudioBuilder and VideoBuilder.

---

## [0.1.0] – 2026-01-08

### Added

- Core `Metronome` module as the single source of truth for timing
- Explicit domain modeling for musical beats:
  - `Beat`
  - `BeatType`
- Audio generation system via `AudioBuilder`
- Video generation system via `VideoBuilder`
- `Composer` module to orchestrate metronome, audio, and video builders
- Configurable BPM and number of bars via `__main__.py`
- Support for distinct sounds per beat type
- Support for distinct images per beat position
- Deterministic beat timing to avoid audio/video drift
- Comprehensive `README.md`
- Contribution guidelines (`CONTRIBUTING.md`)
- High-level architecture diagram
- Clear configuration examples

### Architectural Decisions

- Metronome-driven timing to ensure consistency across all outputs
- Clear separation of concerns between timing, orchestration, audio, and video
- Explicit domain objects instead of implicit timing logic
- No hidden configuration or magic defaults

### Known Limitations

- Fixed time signature (4/4)
- No automated test suite yet
- FPS is currently implicit and not user-configurable
- No CLI arguments (configuration is code-based)
