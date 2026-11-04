import pytest
import requests

from config import API_BASE_URL, CANDIDATE_EMAIL, CANDIDATE_PASSWORD
from pages.auth_page import LoginPage
from pages.jobs_page import JobsPage
from utils.test_helpers import hold_important_page

pytestmark = pytest.mark.smoke


def test_api_health_check():
    response = requests.get(f'{API_BASE_URL}/health', timeout=10)
    assert response.status_code == 200
    assert response.json().get('status') == 'ok'


def test_jobs_endpoint_returns_list():
    response = requests.get(f'{API_BASE_URL}/jobs', timeout=10)
    assert response.status_code == 200
    body = response.json()
    assert 'jobs' in body
    assert isinstance(body['jobs'], list)


def test_homepage_loads_and_shows_jobs(driver):
    jobs_page = JobsPage(driver).open()
    jobs_page.screenshot('smoke_homepage')
    hold_important_page()
    assert jobs_page.find('hero-title').is_displayed()


def test_demo_candidate_login_smoke(driver):
    login_page = LoginPage(driver).open()
    login_page.login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
    hold_important_page()
    login_page.screenshot('smoke_login')
    assert login_page.is_present('nav-logout')
