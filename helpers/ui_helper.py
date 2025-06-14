import time
import allure
import pickle
from faker import Faker
from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from metaclasses.meta_locator import MetaLocator

class UIHelper(metaclass=MetaLocator):

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(self.driver, 15, poll_frequency=1)
        self.actions = ActionChains(self.driver)
        self.fake = Faker()

    def find(self, locator: tuple, wait=False):
        if wait:
            return self.wait.until(EC.visibility_of_element_located(locator))
        else:
            return self.driver.find_element(*locator)

    def find_all(self, locator: tuple, wait=False):
        if wait:
            return self.wait.until(EC.visibility_of_all_elements_located(locator))
        else:
            return self.driver.find_elements(*locator)

    def fill(self, locator: tuple, text: str, clear: bool = False):
        element = self.find(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def click(self, locator: tuple, element_name: str = None):
        """
        This method makes click by element
        :param locator: XPATH
        :param element_name: Name for timeout exception
        :return:
        """
        return self.wait.until(EC.element_to_be_clickable(locator), message=f"{element_name} is not clickable").click()

    def click_via_js(self, locator: tuple):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def screenshot(self, name: str = None):
        """
        Takes a screenshot and attaches it to the Allure report.
        
        Args:
            name (str, optional): Name for the screenshot. If not provided, will use timestamp.
                                 You can use format like 'test_name_step_1' for better organization.
        
        Returns:
            None
        """
        if name is None:
            name = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}"
        
        try:
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(
                body=screenshot,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")

    def wait_for_invisibility(self, locator: tuple, message: str = None):
        return self.wait.until(EC.invisibility_of_element(locator), message=message)

    def wait_for_visibility(self, locator: tuple, message: str = None):
        return self.wait.until(EC.visibility_of_element_located(locator), message=message)

    def wait_for_text_in_web_element(self, element, text: str, message: str = None):
        """
        Ожидает появления текста в веб-элементе.

        :param element: Веб-элемент, в котором будем искать текст.
        :param text: Текст, который мы ожидаем найти в элементе.
        :param message: Сообщение об ошибке, если текст не найден.
        :return: Возвращает элемент, если текст найден.
        """
        try:
            # Ожидаем появления текста в элементе
            self.wait.until(lambda driver: text in element.text)
            return element
        except Exception as e:
            if message:
                raise TimeoutException(message)
            raise e

    def save_cookies(self, cookies_name="temp-cookies"):
        pickle.dump(self.driver.get_cookies(), open(f"cookies/{cookies_name}.pkl", "wb"))

    def load_cookies(self, cookies_name="temp-cookies"):
        cookies = pickle.load(open(f"cookies/{cookies_name}.pkl", "rb"))
        self.driver.delete_all_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def scroll_by(self, x, y):
        self.driver.execute_script(f"window.scrollTo({x}, {y})")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")

    def scroll_to_element(self, locator):
        self.actions.scroll_to_element(self.find(locator))
        self.driver.execute_script("""
        window.scrollTo({
            top: window.scrollY + 500,
        });
        """)