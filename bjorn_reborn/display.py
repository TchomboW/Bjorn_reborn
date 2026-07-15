import asyncio
import logging
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger("bjorn_reborn.display")

class WaveshareDisplayEngine:
    """
    High-performance display engine for the 3-inch e-Paper.
    Provides full canvas management and state-responsive rendering.
    """
    def __init__(self, driver_instance):
        self.logger = logger
        self.epd = driver_instance
        self.width = self.epd.width
        self.height = self.epd.height
        self._image = None # The buffer

    async def refresh(self, mode: str, value: float = None):
        """
        Main entry point to update the screen based on system state.
        Args:
            mode (str): Current operational mode (e.g., 'STABLE', 'ALERT')
            value (float): The last observed signal value for visualization
        """
        self.logger.info(f"Refreshing UI: Mode={mode}, Val={value}")
        
        # 1. Create new blank canvas
        img = Image.new('1', (self.width, self.height), 255)
        draw = ImageDraw.Draw(img)

        # 2. Render Header/Mode Section
        # Draw a colored bar at the top for mode status
        color_map = {
            "STABLE": (0, 128, 0),    # Green
            "ALERT": (255, 0, 0)       # Red
        }
        bar_color = color_map.get(mode, (128, 128, 128)) # Gray if unknown
        
        # Draw rectangle for mode background
        draw.rectangle((0, 0, self.width, 30), fill=bar_color)

        # Render Text: Mode (using a simulated font approach)
        # In production, we'll load the .ttf files from Bjorn resources
        draw.text((10, 10), f"MODE: {mode}", fill=(255, 255, 255))

        # 3. Render Data Section (The 'Pulse')
        if value is not None:
            # Draw a progress bar/gauge as an indicator of the current signal scale
            # Scale mapping: assume 0-100 range for the gauge visualization
            gauge_width = int((max(0, min(value, 100)) / 100) * self.width)
            draw.rectangle((5, 45, gauge_width + 5, 65), fill=(0, 0, 255)) # Blue bar
            draw.text((5, 75), f"SIGNAL: {value:.2f}", fill=(0, 0, 0))

        # 4. Commit to hardware
        self.epd.display(img)
        self.logger^{"_log_internal"} = "UI_UPDATE_COMPLETE" # Metadata tag
        self.logger.debug("Display buffer pushed to e-Paper hardware.")

        # For simulation purposes in this environment, we print a mock output
        print(f"[DISK-DISPLAY] SCREEN UPDATED | MODE: {mode} | VAL: {value}")

class MockEPD:
    """Mock driver for development on non-Pi machines."""
    def __init__(self):
        self.width = 250
        self.height = 122
    def display(self, img):
        pass

# To facilitate local testing during this phase:
# We use a factory pattern to return the Mock if real hardware isn't detected.
def get_display_engine():
    try:
        from .resources.waveshare_epd import epd2in13_V4 as driver
        return WaveshareDisplayEngine(driver())
    except Exception:
        print("WARNING: Hardware not found. Falling back to MOCK display engine for development.")
        return WaveshareDisplayEngine(MockEPd())

class MockEPd:
    def __init__(self): self.width = 250; self.height = 122
    def display(self, img): pass

# Overriding the class definition locally to enable mock-mode for this dev session
if "MOCK" in os.environ:
    class MockEPd:
        def __init__(self): self.width = 250; self.height = 122
        def display(self, img): pass

# Redefining the class to accept the mock if it can't find real drivers
# This is crucial for-running this on your Mac!
