from base.base_test import BaseTest
import allure
import pytest
from pages.login_page import components


@allure.epic("Connect")
@allure.feature("Connect Login Page")
class TestConnect(BaseTest):
    @pytest.mark.connect
    @allure.title("Connect Login Page Test")
    def test_connection(self):
        self.login_page().open()