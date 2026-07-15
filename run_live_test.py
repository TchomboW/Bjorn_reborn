import asyncio
import logging
import sys
import os

# Setup basic imports and paths
sys.path.append("/tmp/Bjor_reborn_refined")

from bjorn_reborn.intel import StatisticsTracker
from bjorn_reborn.connectivity import ConnectivityManager

class BjornOrchestrator:
    def __init__(self, tracker, connectivity):
        self.tracker = tracker
        self.connectivity = connectivity
        self.current_mode = "STABLE" 
        print("Bjorn Engine Initialized with Adaptive Intelligence and Live Connectivity.")

    async def process_signal(self, value):
        if self.tracker.is_anomaly(value, k=3.0):
            print(f"!!! ANOMALY DETECTED !!! [Value: {value}]")
            await self.transition_to("ALERT")
        else:
            self.tracker.add_observation(value)
            if self.current_mode == "ALERT":
                await self.transition_to("STABLE")

    async def transition_to(self, new_mode):
        print(f"MODE TRANSITION: {self.current_mode} -> {new_mode}")
        self.current_mode = new_mode

async def mock_display_refresh(mode, val):
    print(f"  [DISPLAY] Mode: {mode} | Signal Strength: {val}")

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("bjorn")
    
    logger.info("Initializing Bjorn Live System...")
    
    stat_tracker = StatisticsTracker()
    conn_manager = ConnectivityManager()
    engine_brain = BjornOrchestrator(stat_tracker, conn_manager)

    logger.info("Systems Check: [OK]")
    logger.info("Starting continuous telemetry loop (Ctrl+C to stop)...")
    
    try:
        while True:
            current_val = await conn_manager.get_telemetry()
            await engine_brain.process_signal(current_val)
            await mock_display_refresh(engine_brain.current_mode, current_val)
            await asyncio.sleep(2)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received.")
    except Exception as e:
        logger.error(f"System failure: {e}")

if __name__ == "__main__":
    asyncio.run(main())
