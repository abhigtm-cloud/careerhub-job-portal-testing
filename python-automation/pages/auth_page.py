from pages.base_page import BasePage


class LoginPage(BasePage):
    def open(self):
        return super().open('/login')

    def login(self, email: str, password: str):
        self.type_text('input-email', email)
        self.type_text('input-password', password)
        self.click('btn-login')
        return self

    def login_demo(self, role: str = 'candidate'):
        self.click('btn-demo-candidate' if role == 'candidate' else 'btn-demo-recruiter')
        return self

    def get_error(self) -> str:
        return self.find_visible('login-error').text

    def has_error(self) -> bool:
        return self.is_present('login-error')


class RegisterPage(BasePage):
    def open(self):
        return super().open('/register')

    def register(self, name: str, email: str, password: str, role: str = 'candidate', company: str = ''):
        self.select_option('select-role', role)
        self.type_text('input-name', name)
        if role == 'recruiter' and self.is_present('input-company'):
            self.type_text('input-company', company)
        self.type_text('input-email', email)
        self.type_text('input-password', password)
        self.click('btn-register')
        return self

    def get_error(self) -> str:
        return self.find_visible('register-error').text

    def has_error(self) -> bool:
        return self.is_present('register-error')
