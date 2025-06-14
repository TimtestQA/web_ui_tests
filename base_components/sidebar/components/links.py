import allure
from base.base_page import BasePage

class Links(BasePage):

    # Main link for click
    _LINKS_LINK = "//a[text()='Links']"

    # Links items
    _NEWS_FEED_LOCATOR = "//a[@class='menu-section-item-a-newsfeed']"
    _MESSAGES_LOCATOR = "//a[@class='menu-section-item-a-messages']"
    _CONNECT_LOCATOR = "//a[@class='menu-section-item-a-connect']"

    @allure.step("Open 'News Feed' menu")
    def open_news_feed(self):
        self.click_menu_item(self._LINKS_LINK, self._NEWS_FEED_LOCATOR)
        return self

    def open_messages(self):
        self.click_menu_item(self._LINKS_LINK, self._MESSAGES_LOCATOR)
        return self

    @allure.step("Open 'Connect' menu")
    def open_connect(self):
        self.click_menu_item(self._LINKS_LINK, self._CONNECT_LOCATOR)
        return self

