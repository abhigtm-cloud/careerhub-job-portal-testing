import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config import EXPLICIT_WAIT_SECONDS, HOLD_SECONDS, SUPPORTED_BROWSERS


def hold_important_page(seconds: int = HOLD_SECONDS) -> None:
    """Pause so a human reviewer / screen recording can observe the page. Mandatory 6s default."""
    time.sleep(seconds)


def build_driver(browser: str):
    browser = (browser or 'chrome').lower()

    if browser == 'firefox':
        raise ValueError(
            'Firefox is strictly prohibited for this automation suite. Use "chrome" or "edge".'
        )

    if browser not in SUPPORTED_BROWSERS:
        raise NotImplementedError(
            f'Browser "{browser}" is not supported. Supported browsers: {SUPPORTED_BROWSERS}'
        )

    if browser == 'chrome':
        options = ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        service = ChromeService(ChromeDriverManager().install())
        from selenium import webdriver
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    options = EdgeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    service = EdgeService(EdgeChromiumDriverManager().install())
    from selenium import webdriver
    driver = webdriver.Edge(service=service, options=options)
    return driver


def wait_visible(driver, locator, timeout: int = EXPLICIT_WAIT_SECONDS):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_clickable(driver, locator, timeout: int = EXPLICIT_WAIT_SECONDS):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def wait_present(driver, locator, timeout: int = EXPLICIT_WAIT_SECONDS):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


def wait_all_present(driver, locator, timeout: int = EXPLICIT_WAIT_SECONDS):
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator))


def wait_invisible(driver, locator, timeout: int = EXPLICIT_WAIT_SECONDS):
    return WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(locator))


def by_testid(testid: str):
    return (By.CSS_SELECTOR, f'[data-testid="{testid}"]')
