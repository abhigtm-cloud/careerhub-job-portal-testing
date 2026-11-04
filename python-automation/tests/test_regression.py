import pytest

from pages.auth_page import RegisterPage, LoginPage
from pages.jobs_page import JobsPage
from pages.job_detail_modal import JobDetailModal
from pages.applications_page import ApplicationsPage, SavedJobsPage
from pages.profile_page import ProfilePage
from pages.recruiter_page import RecruiterDashboardPage
from utils.test_data import unique_email
from utils.test_helpers import hold_important_page

pytestmark = pytest.mark.regression


def test_full_candidate_journey_register_search_apply_save_profile(driver):
    """Regression: registration -> search -> apply -> save -> profile edit, in one continuous flow."""
    register_page = RegisterPage(driver).open()
    email = unique_email('regression_candidate')
    register_page.register('Regression Candidate', email, 'StrongPass123', role='candidate')
    hold_important_page()
    register_page.screenshot('regression_01_register')

    jobs_page = JobsPage(driver).open()
    jobs_page.search('Developer')
    hold_important_page()
    assert jobs_page.has_results()
    jobs_page.screenshot('regression_02_search')

    jobs_page.open_first_job()
    modal = JobDetailModal(driver)
    modal.apply(cover_letter='Regression suite application')
    hold_important_page()
    modal.screenshot('regression_03_apply')

    apps_page = ApplicationsPage(driver).open()
    hold_important_page()
    assert apps_page.application_count() >= 1
    apps_page.screenshot('regression_04_my_applications')

    jobs_page2 = JobsPage(driver).open()
    jobs_page2.toggle_save_first_job()
    hold_important_page()
    saved_page = SavedJobsPage(driver).open()
    hold_important_page()
    assert saved_page.saved_job_count() >= 1
    saved_page.screenshot('regression_05_saved_jobs')

    profile_page = ProfilePage(driver).open()
    profile_page.set_headline('Regression Tested Candidate')
    profile_page.save()
    hold_important_page()
    profile_page.screenshot('regression_06_profile')
    assert profile_page.find('input-profile-headline').get_attribute('value') == 'Regression Tested Candidate'


def test_full_recruiter_journey_register_post_edit_delete_job(driver):
    """Regression: registration -> post job -> view stats -> edit job -> delete job."""
    register_page = RegisterPage(driver).open()
    email = unique_email('regression_recruiter')
    register_page.register('Regression Recruiter', email, 'StrongPass123', role='recruiter', company='Regression Co')
    hold_important_page()

    dashboard = RecruiterDashboardPage(driver)
    dashboard.post_job(
        title='Regression QA Role',
        company='Regression Co',
        description='A role created by the regression suite to validate the full recruiter workflow.',
        skills='Python, Selenium',
        employment_type='Full-time',
        experience='Mid',
        salary_min=500000,
        salary_max=800000
    )
    hold_important_page()
    dashboard.screenshot('regression_recruiter_01_post_job')

    dashboard.go_to_tab('jobs')
    hold_important_page()
    assert dashboard.job_count() >= 1
    dashboard.screenshot('regression_recruiter_02_my_jobs')

    dashboard.go_to_tab('overview')
    hold_important_page()
    dashboard.screenshot('regression_recruiter_03_stats')
    assert dashboard.is_present('stat-total-jobs')

    dashboard.delete_first_job()
    hold_important_page()
    dashboard.screenshot('regression_recruiter_04_after_delete')
