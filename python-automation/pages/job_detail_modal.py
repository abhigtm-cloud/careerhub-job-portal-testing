from pages.base_page import BasePage


class JobDetailModal(BasePage):
    def is_open(self) -> bool:
        return self.is_present('job-detail-modal')

    def get_title(self) -> str:
        return self.find_visible('modal-job-title').text

    def apply(self, cover_letter: str = ''):
        if cover_letter:
            self.type_text('input-cover-letter', cover_letter)
        self.click('btn-submit-application')
        return self

    def get_apply_error(self) -> str:
        return self.find_visible('apply-error').text

    def has_apply_error(self) -> bool:
        return self.is_present('apply-error')

    def close(self):
        self.click('btn-close-modal')
        return self
