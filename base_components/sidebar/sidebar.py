from base.base_page import BasePage
from base_components.sidebar.components.links import Links
from base_components.sidebar.components.business_page import BusinessPage

class Sidebar(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.links = Links(driver)
        self.business_page = BusinessPage(driver)


