from pages.base_page import BasePage


class JobsPage(BasePage):
    def open(self):
        return super().open('/')

    def search(self, term: str):
        self.type_text('input-search', term)
        self.click('btn-search')
        return self

    def filter_by_company(self, company: str):
        self.type_text('input-filter-company', company)
        return self

    def filter_by_type(self, employment_type: str):
        self.select_option('select-filter-type', employment_type)
        return self

    def filter_by_experience(self, experience: str):
        self.select_option('select-filter-experience', experience)
        return self

    def reset_filters(self):
        self.click('btn-reset-filters')
        return self

    def job_cards(self):
        from selenium.webdriver.common.by import By
        return self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="job-card"]')

    def open_first_job(self):
        self.click('btn-view-job')
        return self

    def has_results(self) -> bool:
        return len(self.job_cards()) > 0

    def is_empty_state(self) -> bool:
        return self.is_present('empty-state')

    def toggle_save_first_job(self):
        self.click('btn-toggle-save')
        return self
