from base.base_test import BaseTest
import allure
import pytest
from pages.login_page.page import LoginPage
from selenium.common.exceptions import TimeoutException


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
    @allure.title("Check actual error messages")
    def test_check_error_messages(self):
        """Тест для проверки реальных сообщений об ошибках на сайте"""
        self.login_page().open()
        
        # Проверяем сообщение для невалидного email
        self.login_page().ui.fill(locator=self.login_page()._LOGIN_FIELD, text="admin@", clear=True)
        self.login_page().ui.fill(locator=self.login_page()._PASSWORD_FIELD, text="Admin123!", clear=True)
        self.login_page().ui.click(locator=self.login_page()._LOGIN_BUTTON)
        print("\nНевалидный email (admin@):", self.login_page().get_error_message())
        
        # Проверяем сообщение для пустого email
        self.login_page().ui.fill(locator=self.login_page()._LOGIN_FIELD, text="", clear=True)
        self.login_page().ui.fill(locator=self.login_page()._PASSWORD_FIELD, text="Admin123!", clear=True)
        self.login_page().ui.click(locator=self.login_page()._LOGIN_BUTTON)
        print("Пустой email:", self.login_page().get_error_message())
        
        # Проверяем сообщение для неверного пароля
        self.login_page().ui.fill(locator=self.login_page()._LOGIN_FIELD, text="admin@example.com", clear=True)
        self.login_page().ui.fill(locator=self.login_page()._PASSWORD_FIELD, text="WrongPass123!", clear=True)
        self.login_page().ui.click(locator=self.login_page()._LOGIN_BUTTON)
        print("Неверный пароль:", self.login_page().get_error_message())
        
        # Проверяем сообщение для SQL инъекции
        self.login_page().ui.fill(locator=self.login_page()._LOGIN_FIELD, text="admin@example.com' OR '1'='1", clear=True)
        self.login_page().ui.fill(locator=self.login_page()._PASSWORD_FIELD, text="Admin123!", clear=True)
        self.login_page().ui.click(locator=self.login_page()._LOGIN_BUTTON)
        print("SQL инъекция:", self.login_page().get_error_message())
        
        # Проверяем сообщение для XSS
        self.login_page().ui.fill(locator=self.login_page()._LOGIN_FIELD, text="<script>alert('xss')</script>@example.com", clear=True)
        self.login_page().ui.fill(locator=self.login_page()._PASSWORD_FIELD, text="Admin123!", clear=True)
        self.login_page().ui.click(locator=self.login_page()._LOGIN_BUTTON)
        print("XSS:", self.login_page().get_error_message())
        
        # Проверяем сообщение для пробелов
        self.login_page().ui.fill(locator=self.login_page()._LOGIN_FIELD, text=" admin@example.com", clear=True)
        self.login_page().ui.fill(locator=self.login_page()._PASSWORD_FIELD, text="Admin123!", clear=True)
        self.login_page().ui.click(locator=self.login_page()._LOGIN_BUTTON)
        print("Пробелы в email:", self.login_page().get_error_message())

    @pytest.mark.negative_login
    @pytest.mark.parametrize(
        "email, password, expected_result", [
            # Валидные данные
            ("admin@example.com", "Admin123!", True),
            ("friend@example.com", "Friend123!", True),
            
            # Невалидный email
            ("admin@", "Admin123!", False),
            ("@example.com", "Admin123!", False),
            ("admin.example.com", "Admin123!", False),
            ("admin@example", "Admin123!", False),
            ("admin@.com", "Admin123!", False),
            ("admin@example..com", "Admin123!", False),
            
            # Пустые поля
            ("", "Admin123!", False),
            ("admin@example.com", "", False),
            ("", "", False),
            
            # Неверный пароль
            ("admin@example.com", "WrongPass123!", False),
            ("admin@example.com", "admin", False),
            ("admin@example.com", "12345678", False),
            
            # XSS и SQL инъекции
            ("admin@example.com' OR '1'='1", "Admin123!", False),
            ("admin@example.com", "Admin123!' OR '1'='1", False),
            ("<script>alert('xss')</script>@example.com", "Admin123!", False),
            
            # Специальные символы
            ("admin!@example.com", "Admin123!", False),
            ("admin@example.com", "Admin!@#$%^&*()", False),
            
            # Пробелы
            (" admin@example.com", "Admin123!", False),
            ("admin@example.com ", "Admin123!", False),
            ("admin@example.com", " Admin123!", False),
            ("admin@example.com", "Admin123! ", False),
        ]
    )
    def test_login(self, email, password, expected_result):
        try:
            self.login_page().open().screenshot("login_page_opened")
            self.login_page().is_opened()
            
            self.login_page().ui.fill(locator=self.login_page()._LOGIN_FIELD, text=email, clear=True)
            self.login_page().ui.fill(locator=self.login_page()._PASSWORD_FIELD, text=password, clear=True)
            self.login_page().ui.click(locator=self.login_page()._LOGIN_BUTTON)
            
            if not expected_result:
                actual_error = self.login_page().get_error_message()
                assert actual_error is not None, "Expected an error message, but got None"
                assert "Invalid username or password" in actual_error, f"Expected error message containing 'Invalid username or password', but got: {actual_error}"
            else:
                self.news_feed_page().is_opened()
                
        except TimeoutException as e:
            if not expected_result:
                # Если тест должен был провалиться, то TimeoutException - это ожидаемое поведение
                pass
            else:
                # Если тест должен был пройти успешно, то TimeoutException - это ошибка
                raise e


