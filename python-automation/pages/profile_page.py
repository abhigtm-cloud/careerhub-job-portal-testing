from pages.base_page import BasePage


class ProfilePage(BasePage):
    def open(self):
        return super().open('/profile')

    def set_name(self, name: str):
        self.type_text('input-profile-name', name)
        return self

    def set_headline(self, headline: str):
        self.type_text('input-profile-headline', headline)
        return self

    def set_phone(self, phone: str):
        self.type_text('input-profile-phone', phone)
        return self

    def add_skill(self, skill: str):
        self.type_text('input-add-skill', skill)
        self.click('btn-add-skill')
        return self

    def remove_first_skill(self):
        self.click('btn-remove-skill')
        return self

    def save(self):
        self.click('btn-save-profile')
        return self

    def skill_chip_count(self) -> int:
        from selenium.webdriver.common.by import By
        return len(self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="skill-chip"]'))
