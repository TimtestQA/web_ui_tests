from base.base_test import BaseTest
import allure
import pytest
from pages.login_page.page import LoginPage


@allure.epic("Connect")
@allure.feature("Connect Page")
class TestConnect(BaseTest):
    @pytest.mark.connect
    @allure.title("Connect Page Test")
    def test_connect_page(self):
        self.login_page().open().screenshot("login_page_opened")
        self.login_page().is_opened()
        
        self.login_page().login_as("admin").screenshot("login_as_admin")
        
        self.sidebar().links.open_connect().screenshot("open_connect")
        self.connect_page().is_opened()