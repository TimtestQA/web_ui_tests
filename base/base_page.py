import allure
from helpers.ui_helper import UIHelper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from metaclasses.meta_locator import MetaLocator

class BasePage(metaclass=MetaLocator):

    _MESSAGE_NOTIFICATION = "//a[@class='ossn-notifications-messages']//span[@class='ossn-notification-container']"
    _SENDER_NAME = "//div[@class='ossn-notification-messages']//div[@class='name']"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15, poll_frequency=1)
        self.ui = UIHelper(self.driver)

    @allure.step("Open page")
    def open(self):
        self.driver.get(self._PAGE_URL)
        return self

    @allure.step("Check if page is opened")
    def is_opened(self):
        print(f"Expected URL: {self._PAGE_URL}")
        print(f"Current URL: {self.driver.current_url}")
        self.wait.until(EC.url_to_be(self._PAGE_URL))
        return self

    @allure.step("Is new messages")
    def is_new_messages(self):
        notification = self.ui.find(self._MESSAGE_NOTIFICATION, True)
        if int(notification.text) != 0:
            notification.click()
        return self

    @allure.step("Check message sender")
    def check_message_sender(self, expected_sender):
        sender = self.ui.find(self._SENDER_NAME, wait=True)
        assert expected_sender in sender.text, f"Expected sender: {expected_sender}, but got {sender.text}"
        return self

    def click_menu_item(self, menu_item_locator, submenu_item_locator):
        try:
            # Сначала проверяем, виден ли подменю элемент
            submenu_item = self.ui.find(submenu_item_locator, wait=True)
        if submenu_item.is_displayed():
                self.ui.click(submenu_item_locator, "Submenu item")
        else:
                # Если подменю не видно, кликаем по основному меню
                self.ui.click(menu_item_locator, "Main menu item")
                # Ждем появления подменю и кликаем
                self.ui.click(submenu_item_locator, "Submenu item after main menu click")
        except Exception as e:
            print(f"Error clicking menu items: {str(e)}")
            raise
        return self

    def screenshot(self, name):
        """
        Takes a screenshot and returns self for method chaining.
        
        Args:
            name (str): Name for the screenshot.
        
        Returns:
            self: Returns self for method chaining.
        """
        self.ui.screenshot(name)
        return self


