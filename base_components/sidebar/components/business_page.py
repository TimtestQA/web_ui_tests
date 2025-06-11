import allure
from base.base_page import BasePage

class BusinessPage(BasePage):

    # Main link for click
    _BUSINESS_PAGE_LINK = "//a[text()='Business Page']"

    # Business Page items
    _CREATE_NEW_PAGE_LOCATOR = "//a//li[text()='Create new page']"

    @allure.step("Open 'Create New Page' menu")
    def create_new_business_page(self):
        self.click_menu_item(self._BUSINESS_PAGE_LINK, self._CREATE_NEW_PAGE_LOCATOR)



