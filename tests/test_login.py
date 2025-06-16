from base.base_test import BaseTest
import allure
import pytest
from pages.login_page.page import LoginPage


@allure.epic("Login")
@allure.feature("Login Page")
class TestLogin(BaseTest):
    @pytest.mark.login
    @allure.title("Login Page Test")
    def test_login_page(self):
        self.login_page().open().screenshot("login_page_opened")
        self.login_page().is_opened()
        
        self.login_page().login_as("admin").screenshot("login_as_admin")
        
        self.sidebar().links.open_news_feed().screenshot("open_news_feed")
        self.news_feed_page().is_opened()


@allure.epic("Login")
@allure.feature("Login Page")
class TestLoginIncorrectData(BaseTest):
    @pytest.mark.negative_login
    @pytest.mark.parametrize(
        "email, password, error_message, expected_result", [
            # Валидные данные
            ("admin@example.com", "Admin123!", None, True),
            ("friend@example.com", "Friend123!", None, True),
            
            # Невалидный email
            ("admin@", "Admin123!", "This value should be a valid email", False),
            ("@example.com", "Admin123!", "This value should be a valid email", False),
            ("admin.example.com", "Admin123!", "This value should be a valid email", False),
            ("admin@example", "Admin123!", "This value should be a valid email", False),
            ("admin@.com", "Admin123!", "This value should be a valid email", False),
            ("admin@example..com", "Admin123!", "This value should be a valid email", False),
            
            # Пустые поля
            ("", "Admin123!", "This value is required", False),
            ("admin@example.com", "", "This value is required", False),
            ("", "", "This value is required", False),
            
            # Неверный пароль
            ("admin@example.com", "WrongPass123!", "Invalid credentials", False),
            ("admin@example.com", "admin", "Invalid credentials", False),
            ("admin@example.com", "12345678", "Invalid credentials", False),
            
            # XSS и SQL инъекции
            ("admin@example.com' OR '1'='1", "Admin123!", "This value should be a valid email", False),
            ("admin@example.com", "Admin123!' OR '1'='1", "Invalid credentials", False),
            ("<script>alert('xss')</script>@example.com", "Admin123!", "This value should be a valid email", False),
            
            # Специальные символы
            ("admin!@example.com", "Admin123!", "This value should be a valid email", False),
            ("admin@example.com", "Admin!@#$%^&*()", "Invalid credentials", False),
            
            # Пробелы
            (" admin@example.com", "Admin123!", "This value should be a valid email", False),
            ("admin@example.com ", "Admin123!", "This value should be a valid email", False),
            ("admin@example.com", " Admin123!", "Invalid credentials", False),
            ("admin@example.com", "Admin123! ", "Invalid credentials", False),
        ]
    )
    def test_login(self, email, password, error_message, expected_result):
        self.login_page().open().screenshot("login_page_opened")
        self.login_page().is_opened()
        
        self.login_page().ui.fill(locator=self.login_page()._LOGIN_FIELD, text=email, clear=True)
        self.login_page().ui.fill(locator=self.login_page()._PASSWORD_FIELD, text=password, clear=True)
        self.login_page().ui.click(locator=self.login_page()._LOGIN_BUTTON)
        
        if not expected_result:
            assert self.login_page().ui.get_text(locator=self.login_page()._ERROR_MESSAGE) == error_message
        else:
            self.news_feed_page().is_opened()


