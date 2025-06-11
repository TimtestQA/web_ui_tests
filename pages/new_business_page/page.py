import allure
from base.base_page import BasePage
from config.links import Links
from config.credentials import Credentials
from pages.new_business_page.components.page_builder import BusinessPageBuilder


class CreateNewBusinessPage(BasePage):

    _PAGE_URL = Links.CREATE_NEW_BUSINESS_PAGE

    _BUSINESS_PAGE_COVER = "//div[@class='business-page-cover']"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.page_builder = BusinessPageBuilder(driver)

    @allure.step("Check if page is created")
    def is_page_created(self):
        self.ui.wait_for_visibility(self._BUSINESS_PAGE_COVER)


    def fill_all_fields(self):
        BusinessPageBuilder(self.driver).set_page_name("Test Page") \
            .set_page_description("Test Description") \
            .set_page_phone("123456789") \
            .set_page_address("Test Address") \
            .set_page_website("http://test.com") \
            .build()

    def fill_required(self):
        BusinessPageBuilder(self.driver).set_page_name("Test Page") \
            .set_page_description("Test Description") \
            .set_page_phone("123456789") \
            .build()