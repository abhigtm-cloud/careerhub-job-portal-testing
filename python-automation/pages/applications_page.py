from pages.base_page import BasePage


class ApplicationsPage(BasePage):
    def open(self):
        return super().open('/applications')

    def application_count(self) -> int:
        from selenium.webdriver.common.by import By
        return len(self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="application-item"]'))

    def is_empty(self) -> bool:
        return self.is_present('empty-state')


class SavedJobsPage(BasePage):
    def open(self):
        return super().open('/saved-jobs')

    def saved_job_count(self) -> int:
        from selenium.webdriver.common.by import By
        return len(self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="job-card"]'))

    def is_empty(self) -> bool:
        return self.is_present('empty-state')

    def remove_first_saved_job(self):
        self.click('btn-toggle-save')
        return self
