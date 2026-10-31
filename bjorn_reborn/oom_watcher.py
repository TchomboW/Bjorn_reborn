"""
OOM (Out-Of-Memory) Watcher for Bjorn Reborn.
Monitors system memory and pauses scanning if free memory drops below a critical threshold (50MB).
Optimized for Raspberry Pi Zero W to prevent OOM killer crashes.
"""
import psutil
import logging
import time
import asyncio
from init_shared import shared_data

logger = logging.getLogger("bjorn_reborn.oom_watcher")

class OOMWatcher:
    def __init__(self, threshold_mb=50, check_interval=5):
        self.threshold_bytes = threshold_mb * 1024 * 1024
        self.check_interval = check_interval
        logger.info(f"OOM Watcher initialized. Threshold: {threshold_mb}MB")

    async def run_monitor(self):
        """Background task that runs continuously to check memory."""
        while True:
            try:
                mem = psutil.virtual_memory()
                free_mb = mem.available / (1024 * 1024)
                
                # If free memory is below threshold, set system_paused
                if free_mb < self.threshold_bytes / (1024 * 1024):
                    if not shared_data.system_paused:
                        logger.warning(f"CRITICAL: Free memory {free_mb:.1f}MB is below {self.threshold_mb}MB. Initiating graceful pause.")
                        shared_data.system_paused = True
                        if hasattr(shared_data, 'bjornstatustext2'):
                            shared_data.bjornstatustext2 = "[PAUSED: LOW MEMORY]"
                else:
                    if shared_data.system_paused:
                        logger.info(f"Memory recovered ({free_mb:.1f}MB). Resuming operations.")
                        shared_data.system_paused = False
                        if hasattr(shared_data, 'bjornstatustext2'):
                            shared_data.bjornstatustext2 = ""
            except Exception as e:
                logger.error(f"OOM Watcher error: {e}")
            
            await asyncio.sleep(self.check_interval)

