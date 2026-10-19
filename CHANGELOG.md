# Change Log

All notable changes to Bjorn Reborn are documented in this file.

## [Unreleased] — 2026-10-19

### 🐛 Bug Fixes

- **Logger**: Fixed handler accumulation bug — handlers now only added once per Logger instance, preventing duplicate log entries on repeated initialization
- **shared.py**: Fixed typo `"web_increment "` → `"web_increment"` (trailing space in config key)
- **shared.py**: Removed duplicate `EPDHelper` initialization that overwrote the display helper on every run
- **shared.py**: Added safe attribute access (`getattr`) for `width`/`height` to prevent `AttributeError` if display init fails before dimensions are set
- **display.py**: Fixed `MockEPD` class name inconsistency (`MockEPd` → `MockEPD`)
- **display.py**: Removed duplicate `epd_helper.display_partial(image)` call that caused redundant screen refreshes
- **display.py** (bjorn_reborn): Removed invalid `self.logger^{"_log_internal"}` metadata tag syntax
- **setup.sh**: Fixed typo in final deployment instruction `system-d` → `systemd`
- **Bjorn.py**: Fixed race condition in orchestrator shutdown — `orchestrator_should_exit` now set **before** joining thread, preventing runaway threads
- **Bjorn.py**: Added 10-second join timeout with warning if orchestrator doesn't stop gracefully

### ✨ Features

- **connectivity.py**: Real RSSI signal strength telemetry via `nmcli` — replaces hardcoded base values with actual wireless signal percentage from the system
- **intel.py**: Anomaly detection now checks **both** upper and lower bounds (`abs(value - mu) > k * sigma`) instead of only upper threshold
- **intel.py**: Added division-by-zero guard when `sigma == 0`
- **comment.py**: Comment delay is now dynamically recalculated on every call for more adaptive timing behavior
- **shared.py**: Upgraded text wrapping engine — now uses `getbbox()` (Pillow ≥ 2.9.0) with `getlength()` fallback, plus a safety break for words that exceed max width

### 🧹 Code Quality

- **orchestrator.py**: Removed ~35 lines of redundant action execution logic — consolidated into `process_alive_ips()` for cleaner control flow
- **setup.sh**: Updated `pil` → `Pillow>=10.3.0` (official package name, `pil` is deprecated)
- **setup.sh**: Added `bettercap-client` dependency for bettercap integration
- **Bjorn.py**: Added lazy import of `WebThread` only when web server is enabled

---

## [Previous Versions]

Refer to git history for earlier changes.
