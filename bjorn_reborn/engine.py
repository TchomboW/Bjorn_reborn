import asyncio
import logging
from .intel import StatisticsTracker
from .connectivity import SmartConnectivityManager

logger = logging.getLogger("bjorn_reborn.engine")

class NetworkTopologyMonitor:
    """Monitors changes in the system's network interfaces."""
    def __init__(self, manager: SmartConnectivityManager):
        self.manager = manager
        self.last_interface = None

    async def check_for_changes(self) -> bool:
        """Checks if a new primary interface has been detected."""
        current_path = await self.manager.get_best_path()
        if not current_path:
            return False
        
        new_name = current_path.name
        if self.last_interface != new_name:
            logger.info(f"NETWORK TOPOLOGY CHANGE DETECTED: {self.last_interface} -> {new_name}")
            self.last_interface = new_name
            return True
        return False

class BjornOrchestrator:
    """The central intelligence-driven state machine."""
    def __init__(self, tracker: StatisticsTracker, connectivity: SmartConnectivityManager):
        self.tracker = tracker
        self.connectivity = connectivity
        self.topology_monitor = NetworkTopologyMonitor(connectivity)
        self.current_mode = "STABLE" 
        logger.info("Bjorn Engine Initialized with Adaptive Intelligence and Multi-Path Awareness.")

    async def process_signal(self, value: float):
        """Primary entry point for a new environmental signal."""
        logger.debug(f"Signal received: {value}")
        
        if self.tracker.is_anomaly(value, k=3.0):
            logger.warning(f"!!! ANOMALY DETECTED !!! [Value: {value}]")
            await self.transition_to("ALERT")
        else:
            self.tracker.add_observation(value)
            if self.current_mode == "ALERT":
                await self.transition_to("STABLE")

    async def transition_to(self, new_mode: str):
        if self.current_mode == new_mode:
            return
        logger.info(f"MODE TRANSITION: {self.current_mode} -> {new_mode}")
        self.current_mode = new_mode
        await self.on_mode_change()

    async def on_mode_change(self):
        pass

async def main_loop(orchestrator: BjornOrchestrator, display=None):
    """The continuous loop that pulls live data and monitors network topology."""
    logger.info("Starting OS-driven Orchestration Loop...")
    try:
        while True:
            # 1. Monitor for Network Topology changes (e.g., plugging in Ethernet)
            await orchestrator.topology_monitor.check_for_changes()

            # 2. Fetch real-world telemetry from the best available path
            current_val = await orchestrator.connectivity.get_telemetry()
            
            # 3. Process the signal through the intelligence layer
            await orchestrator.process_signal(current_val)
            
            # 4. Trigger UI Refresh if a display engine is provided
            if display:
                await display.refresh(orchestrator.current_mode, current_val)
                
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        logger.info("Orchestrator loop terminating.")

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO)
    
    stat_tracker = StatisticsTracker()
    conn_manager = SmartConnectivityManager()
    engine_brain = BjornOrchestrator(stat_tracker, conn_manager)
    
    class MockDisplay:
        async def refresh(self, mode, val):
            print(f"[MOCK DISPLAY] Mode: {mode} | Signal: {val}")

    display_engine = MockDisplay()
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_loop(engine_brain, display_engine))
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
