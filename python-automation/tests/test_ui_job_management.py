import pytest

from pages.jobs_page import JobsPage
from pages.job_detail_modal import JobDetailModal
from utils.test_helpers import hold_important_page

pytestmark = pytest.mark.ui


class TestJobListing:
    def test_jobs_are_displayed_on_landing_page(self, driver):
        page = JobsPage(driver).open()
        hold_important_page()
        page.screenshot('job_listing')
        assert page.has_results()

    def test_search_by_title(self, driver):
        page = JobsPage(driver).open()
        page.search('Developer')
        hold_important_page()
        page.screenshot('search_by_title')
        assert page.has_results()

    def test_search_by_company(self, driver):
        page = JobsPage(driver).open()
        page.search('Nimbus')
        hold_important_page()
        assert page.has_results()

    def test_search_by_skill(self, driver):
        page = JobsPage(driver).open()
        page.search('React')
        hold_important_page()
        assert page.has_results()

    def test_search_with_no_matches_shows_empty_state(self, driver):
        page = JobsPage(driver).open()
        page.search('NoSuchJobTitleZZZ999')
        hold_important_page()
        page.screenshot('search_empty_results')
        assert page.is_empty_state()

    def test_filter_by_employment_type(self, driver):
        page = JobsPage(driver).open()
        page.filter_by_type('Internship')
        hold_important_page()
        for card in page.job_cards():
            assert 'Internship' in card.text

    def test_filter_by_experience_level(self, driver):
        page = JobsPage(driver).open()
        page.filter_by_experience('Senior')
        hold_important_page()
        for card in page.job_cards():
            assert 'Senior' in card.text

    def test_reset_filters_restores_full_list(self, driver):
        page = JobsPage(driver).open()
        page.search('Developer')
        hold_important_page()
        count_filtered = len(page.job_cards())
        page.reset_filters()
        hold_important_page()
        count_reset = len(page.job_cards())
        assert count_reset >= count_filtered


class TestJobDetail:
    def test_opening_job_detail_modal_shows_description(self, driver):
        jobs_page = JobsPage(driver).open()
        jobs_page.open_first_job()
        modal = JobDetailModal(driver)
        hold_important_page()
        modal.screenshot('job_detail_modal')
        assert modal.is_open()
        assert len(modal.get_title()) > 0

    def test_closing_job_detail_modal(self, driver):
        jobs_page = JobsPage(driver).open()
        jobs_page.open_first_job()
        modal = JobDetailModal(driver)
        assert modal.is_open()
        modal.close()
        hold_important_page()
        assert not modal.is_open()
