import allure
from base.base_page import BasePage

class ConnectPage(BasePage):
    _PAGE_URL = "https://example.com/connect"  # Замените на реальный URL

    @allure.step("Check if connect page is opened")
    def is_opened(self):
        self.wait.until(lambda driver: "connect" in driver.current_url.lower())
        return self
 