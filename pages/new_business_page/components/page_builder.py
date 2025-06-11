import allure
from base.base_page import BasePage


class BusinessPageBuilder(BasePage):

    _NAME_FIELD = "//input[@name='name']"
    _DESCRIPTION_FIELD = "//textarea[@name='description']"
    _PHONE_FIELD = "//input[@name='phone']"
    _ADDRESS_FIELD = "//input[@name='address']"
    _WEBSITE_FIELD = "//input[@name='website']"
    _PAGE_TYPE_SELECTOR = "//select[@name='category']"
    _SAVE_BUTTON = "//input[@type='submit']"

    @allure.step("Set page name")
    def set_page_name(self, page_name):
        self.page_name = page_name
        self.ui.fill(self._NAME_FIELD, self.page_name)
        return self

    @allure.step("Set page description")
    def set_page_description(self, page_description):
        self.page_description = page_description
        self.ui.fill(self._DESCRIPTION_FIELD, self.page_description)
        return self

    @allure.step("Set page phone")
    def set_page_phone(self, page_phone):
        self.page_phone = page_phone
        self.ui.fill(self._PHONE_FIELD, self.page_phone)
        return self

    @allure.step("Set page address")
    def set_page_address(self, page_address):
        self.page_address = page_address
        self.ui.fill(self._ADDRESS_FIELD, self.page_address)
        return self

    @allure.step("Set page website")
    def set_page_website(self, page_website):
        self.page_website = page_website
        self.ui.fill(self._WEBSITE_FIELD, self.page_website)
        return self

    @allure.step("Set page type")
    def set_page_type(self, page_type):
        self.page_type = page_type
        self.ui.select(self._PAGE_TYPE_SELECTOR, self.page_type)
        return self

    @allure.step("Save page")
    def build(self):
        self.ui.click(self._SAVE_BUTTON)


