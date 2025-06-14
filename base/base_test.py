from pages.login_page.page import LoginPage
from pages.news_feed_page.page import NewsFeedPage
from base_components.sidebar.sidebar import Sidebar
from pages.new_business_page.page import CreateNewBusinessPage
from pages.messages_page.page import MessagesPage
from pages.connect_page.page import ConnectPage
from helpers.ui_helper import UIHelper

class BaseTest:

    def setup_method(self):
        # Helpers
        self.ui = UIHelper(self.driver)
        
        # Pages
        self.login_page = lambda driver=self.driver: LoginPage(driver)
        self.news_feed_page = lambda driver=self.driver: NewsFeedPage(driver)
        self.new_business_page = lambda driver=self.driver: CreateNewBusinessPage(driver)
        self.messages_page = lambda driver=self.driver: MessagesPage(driver)
        self.connect_page = lambda driver=self.driver: ConnectPage(driver)

        # Components
        self.sidebar = lambda driver=self.driver: Sidebar(driver)