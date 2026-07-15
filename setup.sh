#!/bin/bash

# ==============================================================================
# BJORN REBORN - PRODUCTION DEPLOYMENT SCRIPT (PHASE 4)
# Target Platform: Raspberry Pi OS (64-bit / ARM64)
# Function: System provisioning, dependency isolation, and service orchestration.
# ==============================================================================

set -e # Exit on any error

# --- COLOR SCHEME ---
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo -e "${BLUE}=============================================="
echo -e "       BJORN REBORN: SYSTEM PROVISIONING      "
echo -e "==============================================${NC}"

# --- phase 1: ENVIRONMENT VALIDATION ---
log "Starting system validation..."

# 1. Check Architecture
ARCH=$(uname -m)
if [[ "$ARCH" != "aarch64" ]]; then
    warn "Current architecture is $ARCH. Bjorn is optimized for aarch64 (64-bit)."
    echo "Proceeding anyway, but performance may be degraded."
fi

# 2. Check Connectivity (Required for dependency installation)
log "Testing internet connectivity..."
if ! ping -c 1 8.8.8.8 > /dev/null 2>&1; then
    error "No internet connection detected. Cannot install dependencies."
fi
success "Internet connectivity verified."

# --- phase 2: DIRECTORY & VIRTUAL ENV SETUP ---
log "Setting up isolated execution environment..."

# Ensure we are in the project root
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [ -d ".venv" ]; then
    warn "Existing virtual environment found. Re-initializing..."
    rm -rf .venv
fi

python3 -m venv .venv
success "Virtual environment created at $PROJECT_DIR/.venv"

# --- phase 3: DEPENDENCY INSTALLATION ---
log "Installing intelligence stack (this may take a few minutes)..."

# Using the venv pip directly to avoid activation issues in scripts
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install pil numpy asyncio  # Core Bjorn dependencies

success "Dependency installation complete."

# --- phase 4: SYSTEMD SERVICE ORCHESTRATION ---
log "Configuring system-level orchestration (Systemd)..."

SERVICE_FILE="/etc/systemd/system/bjorn.service"

# Note: This requires sudo to write to /etc/systemd/system/
# We will create a template and instruct the user to move it, 
# OR attempt to write if they run as root.

cat <<EOF > bjorn_worker.service
[Unit]
Description=Bjorn Reborn Adaptive Intelligence Engine
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/.venv/bin/python $PROJECT_DIR/bjorn_reborn/engine.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

log "Systemd service file generated as bjorn_worker.service"
warn "To enable auto-start on boot, run the following commands:"
echo -e "${YELLOW}  sudo mv bjorn_worker.service /etc/systemd/system/bjorn.service${NC}"
echo -e "${YELLOW}  sudo systemctl daemon-reload${NC}"
echo -e "${YELLOW}  sudo systemctl enable bjorn.service${NC}"

# --- phase 5: FINAL CHECK ---
log "Finalizing deployment..."

if [ -f "bjorn_reborn/engine.py" ]; then
    success "Engine found: $PROJECT_DIR/bjorn_reborn/engine.py"
else
    error "Core engine file missing! Check your directory structure."
fi

echo -e "${BLUE}=============================================="
echo -e "       DEPLOYMENT PREPARED SUCCESSFULLY      "
echo -e "==============================================${NC}"
echo -e "${GREEN}Final Step:${NC} Run: ${YELLOW}sudo mv bjorn_worker.service /etc/system-d/system/bjorn.service${NC}"
echo -e "${GREEN}Then run:${NC} ${YELLOW}sudo systemctl start bjorn${NC}"
