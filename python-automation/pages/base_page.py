from config import FRONTEND_URL, HOLD_SECONDS
from utils.test_helpers import wait_visible, wait_clickable, wait_present, by_testid, hold_important_page
from utils.screenshot_manager import ScreenshotManager


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, path: str = ''):
        self.driver.get(f'{FRONTEND_URL}{path}')
        return self

    def find(self, testid: str, timeout: int = 15):
        return wait_present(self.driver, by_testid(testid), timeout)

    def find_visible(self, testid: str, timeout: int = 15):
        return wait_visible(self.driver, by_testid(testid), timeout)

    def click(self, testid: str, timeout: int = 15):
        element = wait_clickable(self.driver, by_testid(testid), timeout)
        element.click()
        return element

    def type_text(self, testid: str, text: str, clear_first: bool = True, timeout: int = 15):
        element = wait_visible(self.driver, by_testid(testid), timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def select_option(self, testid: str, value: str, timeout: int = 15):
        from selenium.webdriver.support.ui import Select
        element = wait_visible(self.driver, by_testid(testid), timeout)
        Select(element).select_by_value(value)
        return element

    def is_present(self, testid: str, timeout: int = 6) -> bool:
        """Polls for up to `timeout` seconds before concluding an element is absent.

        A plain instant find_element() races against the app's async state updates
        (e.g. an error banner appearing a few hundred ms after a form submit), so this
        waits briefly instead of failing on timing alone.
        """
        from selenium.common.exceptions import TimeoutException
        try:
            wait_present(self.driver, by_testid(testid), timeout)
            return True
        except TimeoutException:
            return False

    def screenshot(self, name: str) -> str:
        return ScreenshotManager.capture(self.driver, name)

    def hold(self, seconds: int = HOLD_SECONDS):
        hold_important_page(seconds)
        return self

    def set_viewport(self, width: int, height: int):
        self.driver.set_window_size(width, height)
        return self
