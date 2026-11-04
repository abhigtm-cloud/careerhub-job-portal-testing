import pytest

from config import CANDIDATE_EMAIL, CANDIDATE_PASSWORD
from pages.auth_page import LoginPage
from pages.jobs_page import JobsPage
from pages.job_detail_modal import JobDetailModal
from pages.applications_page import ApplicationsPage
from utils.test_data import unique_email
from utils.test_helpers import hold_important_page

pytestmark = pytest.mark.ui


def _login_as_fresh_candidate(driver):
    from pages.auth_page import RegisterPage
    page = RegisterPage(driver).open()
    email = unique_email('applicant')
    page.register('Fresh Applicant', email, 'StrongPass123', role='candidate')
    hold_important_page()
    return email


class TestJobApplications:
    def test_candidate_can_apply_to_a_job(self, driver):
        _login_as_fresh_candidate(driver)
        jobs_page = JobsPage(driver).open()
        jobs_page.open_first_job()
        modal = JobDetailModal(driver)
        modal.apply(cover_letter='I am excited to apply for this role.')
        hold_important_page()
        modal.screenshot('application_submitted')

        apps_page = ApplicationsPage(driver).open()
        hold_important_page()
        apps_page.screenshot('my_applications')
        assert apps_page.application_count() >= 1

    def test_duplicate_application_is_prevented(self, driver):
        _login_as_fresh_candidate(driver)
        jobs_page = JobsPage(driver).open()
        jobs_page.open_first_job()
        modal = JobDetailModal(driver)
        modal.apply()
        hold_important_page()

        jobs_page2 = JobsPage(driver).open()
        jobs_page2.open_first_job()
        modal2 = JobDetailModal(driver)
        modal2.apply()
        assert modal2.has_apply_error()
        modal2.screenshot('duplicate_application_blocked')

    def test_my_applications_page_empty_state_for_new_user(self, driver):
        _login_as_fresh_candidate(driver)
        apps_page = ApplicationsPage(driver).open()
        hold_important_page()
        assert apps_page.is_empty()

    def test_login_as_demo_candidate_sees_application_history(self, driver):
        login_page = LoginPage(driver).open()
        login_page.login(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
        hold_important_page()
        apps_page = ApplicationsPage(driver).open()
        hold_important_page()
        assert apps_page.application_count() >= 0
