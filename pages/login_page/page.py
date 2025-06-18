import allure
from base.base_page import BasePage
from config.links import Links
from config.credentials import Credentials
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LoginPage(BasePage):

    _PAGE_URL = Links.LOGIN_PAGE

    _LOGIN_BUTTON = "//input[@type='submit']"
    _LOGIN_FIELD = "//input[@name='username']"
    _PASSWORD_FIELD = "//input[@name='password']"
    _ERROR_MESSAGE = "//div[@class='alert alert-danger']/strong"

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

    @allure.step("Get error message")
    def get_error_message(self):
        """
        Получает текст сообщения об ошибке.
        
        Returns:
            str: Текст сообщения об ошибке или None, если сообщение не найдено
        """
        try:
            return self.ui.get_text(self._ERROR_MESSAGE, wait=True)
        except:
            return None
