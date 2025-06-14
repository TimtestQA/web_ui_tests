import allure
from base.base_page import BasePage
from config.links import Links
from config.credentials import Credentials


class LoginPage(BasePage):

    _PAGE_URL = Links.LOGIN_PAGE

    _LOGIN_BUTTON = "//input[@type='submit']"
    _LOGIN_FIELD = "//input[@name='username']"
    _PASSWORD_FIELD = "//input[@name='password']"

    @allure.step("Click login button")
    def login_as(self, user_type):
        if user_type == "admin":
            self.ui.fill(locator=self._LOGIN_FIELD, text=Credentials.ADMIN_LOGIN, clear=True)
            self.ui.fill(locator=self._PASSWORD_FIELD, text=Credentials.ADMIN_PASSWORD, clear=True)
            self.ui.click(self._LOGIN_BUTTON, "Login button")
        elif user_type == "friend":
            self.ui.fill(locator=self._LOGIN_FIELD, text=Credentials.FRIEND_LOGIN, clear=True)
            self.ui.fill(locator=self._PASSWORD_FIELD, text=Credentials.FRIEND_PASSWORD, clear=True)
            self.ui.click(self._LOGIN_BUTTON, "Login button")
        return self
