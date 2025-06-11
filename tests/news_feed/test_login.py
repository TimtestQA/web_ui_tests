from base.base_test import BaseTest
import allure
import pytest
from pages.login_page import components


@allure.epic("Login")
@allure.feature("Login Page")
class TestLogin(BaseTest):
    @pytest.mark.login
    @allure.title("Login Page Test")
    def test_login_page(self):
        self.login_page().open()
        self.ui.screenshot("login_page_opened")
        self.login_page().is_opened()
        
        self.login_page().login_as("admin")
        self.ui.screenshot("after_login")
        
        self.sidebar().links.open_news_feed()
        self.ui.screenshot("news_feed_page")
        self.news_feed_page().is_opened()

