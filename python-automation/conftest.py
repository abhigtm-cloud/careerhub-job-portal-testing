import pytest

from config import BROWSER, MONGODB_URI
from utils.test_helpers import build_driver
from utils.screenshot_manager import ScreenshotManager


@pytest.fixture
def driver():
    drv = build_driver(BROWSER)
    yield drv
    drv.quit()


@pytest.fixture
def mongo_db():
    from pymongo import MongoClient
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    db = client.get_default_database()
    yield db
    client.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver is not None:
            try:
                path = ScreenshotManager.capture(driver, f'FAILURE_{item.name}')
                if hasattr(item.config, '_html'):
                    html = f'<div><img src="{path}" style="width:400px;" /></div>'
                    extra = getattr(report, 'extra', [])
                    report.extra = extra
            except Exception:
                pass
