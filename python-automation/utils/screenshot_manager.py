from datetime import datetime

from config import SCREENSHOTS_DIR


class ScreenshotManager:
    """Captures genuine browser screenshots with descriptive, timestamped filenames."""

    @staticmethod
    def capture(driver, name: str) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        safe_name = ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
        filename = f'{safe_name}_{timestamp}.png'
        path = SCREENSHOTS_DIR / filename
        driver.save_screenshot(str(path))
        return str(path)
