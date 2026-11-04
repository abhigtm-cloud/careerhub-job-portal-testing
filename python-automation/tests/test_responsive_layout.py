import pytest

from config import VIEWPORTS
from pages.jobs_page import JobsPage
from pages.auth_page import LoginPage
from utils.test_helpers import hold_important_page, by_testid

pytestmark = pytest.mark.responsive


@pytest.mark.parametrize('viewport_name', ['desktop', 'tablet', 'mobile'])
def test_jobs_page_renders_without_horizontal_overflow(driver, viewport_name):
    width, height = VIEWPORTS[viewport_name]
    page = JobsPage(driver)
    page.set_viewport(width, height)
    page.open()
    hold_important_page()
    page.screenshot(f'responsive_jobs_{viewport_name}')

    scroll_width = driver.execute_script('return document.documentElement.scrollWidth;')
    client_width = driver.execute_script('return document.documentElement.clientWidth;')
    assert scroll_width <= client_width + 5, (
        f'Horizontal overflow detected at {viewport_name} viewport '
        f'({width}x{height}): scrollWidth={scroll_width}, clientWidth={client_width}'
    )
    assert page.has_results() or page.is_empty_state()


@pytest.mark.parametrize('viewport_name', ['desktop', 'tablet', 'mobile'])
def test_navbar_is_usable_at_each_viewport(driver, viewport_name):
    width, height = VIEWPORTS[viewport_name]
    page = JobsPage(driver)
    page.set_viewport(width, height)
    page.open()
    hold_important_page()

    if viewport_name in ('mobile', 'tablet'):
        assert page.find('navbar-toggler').is_displayed()
        page.click('navbar-toggler')
        hold_important_page()
        page.screenshot(f'responsive_{viewport_name}_nav_open')
        assert page.find_visible('nav-login').is_displayed()
    else:
        assert page.find('nav-login').is_displayed()


def test_login_form_usable_on_mobile(driver):
    width, height = VIEWPORTS['mobile']
    page = LoginPage(driver)
    page.set_viewport(width, height)
    page.open()
    hold_important_page()
    page.screenshot('responsive_login_mobile')
    assert page.find('login-card').is_displayed()
