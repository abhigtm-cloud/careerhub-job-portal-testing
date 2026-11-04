import pytest

from config import CANDIDATE_EMAIL, CANDIDATE_PASSWORD, RECRUITER_EMAIL, RECRUITER_PASSWORD
from pages.auth_page import LoginPage, RegisterPage
from utils.test_data import unique_email, INVALID_EMAILS, WEAK_PASSWORDS
from utils.test_helpers import hold_important_page

pytestmark = pytest.mark.ui


class TestRegistration:
    def test_candidate_registration_positive(self, driver):
        page = RegisterPage(driver).open()
        page.register('Automation Candidate', unique_email('cand'), 'StrongPass123', role='candidate')
        hold_important_page()
        page.screenshot('register_candidate_success')
        assert page.is_present('nav-logout')

    def test_recruiter_registration_positive(self, driver):
        page = RegisterPage(driver).open()
        page.register('Automation Recruiter', unique_email('rec'), 'StrongPass123', role='recruiter', company='QA Corp')
        hold_important_page()
        page.screenshot('register_recruiter_success')
        assert page.is_present('nav-logout')

    def test_registration_rejects_duplicate_email(self, driver):
        email = unique_email('dup')
        page = RegisterPage(driver).open()
        page.register('First User', email, 'StrongPass123', role='candidate')
        hold_important_page()

        page.driver.delete_all_cookies()
        page.driver.execute_script('window.localStorage.clear();')

        page2 = RegisterPage(driver).open()
        page2.register('Second User', email, 'StrongPass123', role='candidate')
        assert page2.has_error()

    @pytest.mark.parametrize('bad_email', INVALID_EMAILS)
    def test_registration_rejects_invalid_email(self, driver, bad_email):
        page = RegisterPage(driver).open()
        page.register('Invalid Email User', bad_email, 'StrongPass123', role='candidate')
        assert page.has_error()

    @pytest.mark.parametrize('weak_password', WEAK_PASSWORDS)
    def test_registration_rejects_weak_password(self, driver, weak_password):
        page = RegisterPage(driver).open()
        page.register('Weak Password User', unique_email('weak'), weak_password, role='candidate')
        assert page.has_error()

    def test_registration_rejects_empty_name(self, driver):
        page = RegisterPage(driver).open()
        page.register('', unique_email('noname'), 'StrongPass123', role='candidate')
        assert page.has_error()


class TestLogin:
    def test_candidate_login_positive(self, driver):
        page = LoginPage(driver).open()
        page.login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
        hold_important_page()
        page.screenshot('login_candidate_success')
        assert page.is_present('nav-logout')
        assert page.is_present('nav-applications')

    def test_recruiter_login_positive(self, driver):
        page = LoginPage(driver).open()
        page.login(RECRUITER_EMAIL, RECRUITER_PASSWORD)
        hold_important_page()
        page.screenshot('login_recruiter_success')
        assert page.is_present('nav-recruiter-dashboard')

    def test_login_rejects_incorrect_password(self, driver):
        page = LoginPage(driver).open()
        page.login(CANDIDATE_EMAIL, 'WrongPassword999')
        assert page.has_error()
        page.screenshot('login_invalid_credentials')

    def test_login_rejects_unknown_email(self, driver):
        page = LoginPage(driver).open()
        page.login('doesnotexist@careerhub-test.com', 'SomePassword123')
        assert page.has_error()

    def test_demo_candidate_login_button(self, driver):
        page = LoginPage(driver).open()
        page.login_demo('candidate')
        hold_important_page()
        assert page.is_present('nav-logout')

    def test_demo_recruiter_login_button(self, driver):
        page = LoginPage(driver).open()
        page.login_demo('recruiter')
        hold_important_page()
        assert page.is_present('nav-recruiter-dashboard')


class TestLogout:
    def test_logout_clears_session(self, driver):
        page = LoginPage(driver).open()
        page.login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
        hold_important_page()
        page.click('nav-logout')
        hold_important_page()
        assert page.is_present('nav-login')
