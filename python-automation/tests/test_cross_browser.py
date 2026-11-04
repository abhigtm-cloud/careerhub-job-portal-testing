import pytest

from pages.jobs_page import JobsPage
from pages.auth_page import LoginPage
from utils.test_helpers import build_driver, hold_important_page
from config import CANDIDATE_EMAIL, CANDIDATE_PASSWORD

pytestmark = pytest.mark.cross_browser


@pytest.fixture
def cross_browser_driver(request):
    drv = build_driver(request.param)
    yield drv
    drv.quit()


@pytest.mark.parametrize('cross_browser_driver', ['chrome', 'edge'], indirect=True)
def test_jobs_page_loads_on_each_browser(cross_browser_driver):
    page = JobsPage(cross_browser_driver).open()
    hold_important_page()
    page.screenshot(f'cross_browser_jobs_{cross_browser_driver.name}')
    assert page.has_results()


@pytest.mark.parametrize('cross_browser_driver', ['chrome', 'edge'], indirect=True)
def test_login_works_on_each_browser(cross_browser_driver):
    page = LoginPage(cross_browser_driver).open()
    page.login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
    hold_important_page()
    page.screenshot(f'cross_browser_login_{cross_browser_driver.name}')
    assert page.is_present('nav-logout')


def test_firefox_is_explicitly_rejected():
    with pytest.raises(ValueError):
        build_driver('firefox')


def test_unsupported_browser_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        build_driver('safari')
