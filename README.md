# Bjorn Reborn 🤖

**An Adaptive Intelligence Orchestrator for Raspberry Pi Zero W.**

Bjorn Reborn is a high-performance, lightweight intelligence engine designed specifically for the Raspberry Pi Zero W ecosystem. Optimized for **Raspberry Pi OS (64-bit)**, it leverages adaptive statistical analysis to detect environmental changes and provides real-time telemetry through e-Paper display interfaces.

---

## ✨ Key Features

*   **🧠 Adaptive Intelligence**: Uses a rolling statistics tracker (`intel.py`) to detect anomalies in signal strength or network availability.
*   **📡 Live Connectivity Sensing**: Implements an L7 connectivity manager (`connectivity.py`) that monitors real-world network health.
*   **🖼️ Intelligent Display Interface**: Optimized for Waveshare e-Paper displays, providing high-contrast, low-power status updates including mode transitions and signal gauges.
*   **🚀 Production-Ready Deployment**: Includes automated provisioning via `setup.sh` and `systemd` service orchestration for autonomous operation.

---

## 🛠️ Hardware Requirements

To achieve full functionality as designed, the following hardware is recommended:

1.  **Single Board Computer**: Raspberry Pi Zero W (or any compatible ARM64 device).
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
Run the automated setup script. This will create an isolated virtual environment and install all required intelligence dependencies (NumPy, Pillow, etc.).
```bash
chmod +x setup.sh
./setup.sh
```

### 4. Deploy as a Background Service
To ensure Bjorn starts automatically on boot and recovers if it ever crashes, we use `systemd`. Run these commands:
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

The system follows a modular, layered approach:

*   **`bjorn_reborn/intel.py`**: The statistical brain. It tracks observations and calculates real-time anomalies.
*   **`bjorn_reborn/connectivity.py`**: The nervous system. It probes the network to provide live environmental telemetry.
*   **`bjorn_reborn/engine.py`**: The central orchestrator. It processes signals, manages state transitions (e.g., `STABLE` $\leftrightarrow$ `ALERT`), and drives the loop.
*   **`bjorn_reborn/display.py`**: The face. Translates internal states into visual information for e-Paper hardware.

---

## 📄 License
This project is licensed under the MIT License.
