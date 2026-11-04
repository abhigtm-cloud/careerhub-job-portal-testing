import pytest

from pages.auth_page import RegisterPage
from pages.jobs_page import JobsPage
from pages.applications_page import SavedJobsPage
from pages.profile_page import ProfilePage
from utils.test_data import unique_email, BOUNDARY_STRINGS
from utils.test_helpers import hold_important_page

pytestmark = pytest.mark.ui


def _login_as_fresh_candidate(driver):
    page = RegisterPage(driver).open()
    page.register('Saved Jobs Candidate', unique_email('saver'), 'StrongPass123', role='candidate')
    hold_important_page()


class TestSavedJobs:
    def test_saved_jobs_page_empty_for_new_user(self, driver):
        _login_as_fresh_candidate(driver)
        saved_page = SavedJobsPage(driver).open()
        hold_important_page()
        saved_page.screenshot('saved_jobs_empty')
        assert saved_page.is_empty()

    def test_save_a_job_and_view_it(self, driver):
        _login_as_fresh_candidate(driver)
        jobs_page = JobsPage(driver).open()
        jobs_page.toggle_save_first_job()
        hold_important_page()

        saved_page = SavedJobsPage(driver).open()
        hold_important_page()
        saved_page.screenshot('saved_jobs_with_item')
        assert saved_page.saved_job_count() >= 1

    def test_remove_a_saved_job(self, driver):
        _login_as_fresh_candidate(driver)
        jobs_page = JobsPage(driver).open()
        jobs_page.toggle_save_first_job()
        hold_important_page()

        saved_page = SavedJobsPage(driver).open()
        hold_important_page()
        saved_page.remove_first_saved_job()
        hold_important_page()
        assert saved_page.is_empty() or saved_page.saved_job_count() == 0


class TestProfile:
    def test_edit_profile_headline_and_phone(self, driver):
        _login_as_fresh_candidate(driver)
        profile_page = ProfilePage(driver).open()
        profile_page.set_headline('Aspiring QA Automation Engineer')
        profile_page.set_phone('9988776655')
        profile_page.save()
        hold_important_page()
        profile_page.screenshot('profile_updated')
        assert profile_page.find('input-profile-headline').get_attribute('value') == 'Aspiring QA Automation Engineer'

    def test_add_and_remove_skill(self, driver):
        _login_as_fresh_candidate(driver)
        profile_page = ProfilePage(driver).open()
        profile_page.add_skill('Selenium')
        hold_important_page()
        count_after_add = profile_page.skill_chip_count()
        assert count_after_add >= 1

        profile_page.remove_first_skill()
        hold_important_page()
        count_after_remove = profile_page.skill_chip_count()
        assert count_after_remove == count_after_add - 1

    def test_profile_rejects_invalid_phone(self, driver):
        _login_as_fresh_candidate(driver)
        profile_page = ProfilePage(driver).open()
        profile_page.set_phone('not-a-phone')
        profile_page.save()
        assert profile_page.is_present('profile-error')

    def test_profile_handles_boundary_headline_length(self, driver):
        _login_as_fresh_candidate(driver)
        profile_page = ProfilePage(driver).open()
        profile_page.set_headline(BOUNDARY_STRINGS['max_name_length'])
        profile_page.save()
        hold_important_page()
        assert not profile_page.is_present('profile-error')
