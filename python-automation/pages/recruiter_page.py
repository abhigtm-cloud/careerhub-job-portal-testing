from pages.base_page import BasePage


class RecruiterDashboardPage(BasePage):
    def open(self):
        return super().open('/recruiter')

    def go_to_tab(self, tab: str):
        self.click(f'tab-{tab}')
        return self

    def post_job(self, title, company, description, skills='', location='Remote',
                 employment_type=None, experience=None, salary_min='', salary_max=''):
        self.go_to_tab('post')
        self.type_text('input-job-title', title)
        self.type_text('input-job-company', company)
        self.type_text('input-job-location', location)
        if employment_type:
            self.select_option('select-job-type', employment_type)
        if experience:
            self.select_option('select-job-experience', experience)
        self.type_text('input-job-skills', skills)
        self.type_text('input-job-salary-min', str(salary_min))
        self.type_text('input-job-salary-max', str(salary_max))
        self.type_text('input-job-description', description)
        self.click('btn-post-job')
        return self

    def get_post_job_error(self) -> str:
        return self.find_visible('post-job-error').text

    def has_post_job_error(self) -> bool:
        return self.is_present('post-job-error')

    def delete_first_job(self):
        self.go_to_tab('jobs')
        self.click('btn-delete-job')
        self.driver.switch_to.alert.accept()
        return self

    def edit_first_job(self):
        self.go_to_tab('jobs')
        self.click('btn-edit-job')
        return self

    def view_first_job_applications(self):
        self.go_to_tab('jobs')
        self.click('btn-view-applications')
        return self

    def job_count(self) -> int:
        from selenium.webdriver.common.by import By
        return len(self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="recruiter-job-item"]'))
