# Bjorn Reborn 🤖

**An Adaptive Intelligence Orchestrator specialized for Raspberry Pi Zero W.**

Bjorn Reborn is a high-performance, lightweight intelligence engine designed specifically for the **Raspberry Pi Zero W (512MB RAM)** ecosystem. Optimized for **Raspberry Pi OS (64-bit)**, it leverages adaptive statistical analysis, concurrent action dispatching, and aggressive memory management to ensure autonomous operation without crashes.

---

## ✨ Key Features

*   **🛡️ Pi Zero W Optimized**: Hard-coded concurrency limits (3 workers, 8 threads) to prevent CPU thrashing on single-core architectures.
*   **🛡️ OOM (Out-Of-Memory) Protection**: Integrated memory watcher that automatically pauses scanning if free RAM drops below **50MB**, preventing system crashes.
*   **🧠 Adaptive Intelligence**: Uses a rolling statistics tracker (`intel.py`) to detect anomalies in signal strength or network availability.
*   **📡 Live Connectivity Sensing**: Implements a non-blocking L7 connectivity manager (`connectivity.py`) with real RSSI telemetry via `nmcli`.
*   **💾 Ultra-Lightweight Data**: Replaced heavy `pandas` dependencies with standard library `csv` module, reducing RAM usage from ~100MB to <5MB.
*   **🧵 Safe Parallelism**: Blocking I/O operations (SSH, SMB, FTP) are wrapped in a `ThreadPoolExecutor` to keep the main event loop responsive.
*   **🖼️ Intelligent Display Interface**: Optimized for Waveshare e-Paper displays, providing high-contrast, low-power status updates.
*   **🚀 Production-Ready Deployment**: Includes automated provisioning via `scripts/setup.sh` and `systemd` service orchestration.

---

## 🛠️ Hardware Requirements

To achieve full functionality as designed, the following hardware is recommended:

1.  **Single Board Computer**: Raspberry Pi Zero W (or any compatible ARM64 device with <1GB RAM).
2.  **Display**: Waveshare e-Paper Display (SPI interface).
3.  **OS Requirement**: **Raspberry Pi OS (64-bit)**. *The software is highly optimized for the 64-bit instruction set.*

---

## 🚀 Installation & Deployment Guide

### 1. Prepare your Raspberry Pi
Flash your SD card with a clean install of **Raspberry Pi OS (64-bit)**. Ensure you have SSH access or a terminal available.

### 2. Clone the Repository
```bash
git clone https://github.com/TchomboW/Bjorn_reborn
cd Bjorn_reborn
```

### 3. Provision the Environment
Run the automated setup script from the `scripts/` directory. This will create an isolated virtual environment and install all required intelligence dependencies (NumPy, Pillow, psutil, etc.).
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 4. Deploy as a Background Service
To ensure Bjorn starts automatically on boot and recovers if it ever crashes, we use `systemd`.
```bash
# Move the bundled service file to the system directory
sudo mv bjor_worker.service /etc/systemd/system/bjorn.service

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable bjorn
sudo systemctl start bjorn
```

### 5. Monitor Status
You can monitor your engine's logs at any time using:
```bash
journalctl -u bjorn -f
```

---

## 🏗️ Architecture Overview

The system follows a modular, event-driven approach decoupled for maximum stability on low-resource hardware:

*   **`bjorn_reborn/intel.py`**: The statistical brain. It tracks observations and calculates real-time anomalies.
*   **`bjorn_reborn/connectivity.py`**: The nervous system. It probes the network asynchronously to provide live environmental telemetry.
*   **`bjorn_reborn/engine.py`**: The state machine. It processes signals, manages state transitions (e.g., `STABLE` ↔ `ALERT`), and drives the loop.
*   **`orchestrator.py`**: The action scheduler. It dispatches actions (scanning, credential testing) via a `ThreadPoolExecutor` (max 3 workers) to prevent blocking the UI loop.
*   **`display.py`**: The face. Translates internal states into visual information for e-Paper hardware using lightweight CSV parsing.
*   **`actions/`**: Specialized modules for scanning (SSH, FTP, SMB, RDP, SQL) that run in isolated threads.
*   **`utils/`**: Shared utilities including the memory monitoring logic and logging infrastructure.

---

## 📁 Repository Structure

The codebase has been tidied for clarity and maintainability:

*   `📂 scripts/`: Shell scripts for installation, setup, and maintenance.
*   `📂 utils/`: Python utility modules (shared state, logging, config loading).
*   `📂 conf/`: Configuration files, requirements, and versioning.
*   `📂 actions/`: All offensive/intelligence action modules.
*   `📂 bjorn_reborn/`: Core intelligence components (engine, intel, connectivity).
*   `📂 web/`: Frontend assets for the web dashboard.

---

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and recent improvements.

---

## 📄 License
This project is licensed under the MIT License.
