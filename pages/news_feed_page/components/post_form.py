import time
import allure
from base.base_page import BasePage

class PostFormComponent(BasePage):

    _POST_TEXTAREA = "//textarea[@name='post']"

    _TAG_FRIEND_BUTTON = "//li[contains(@class, 'tag-friend')]"
    _TAG_FRIEND_FIELD = "//input[@id='token-input-ossn-wall-friend-input']"

    _ADD_IMAGE_BUTTON = "//li[contains(@class, 'menu-photo')]"
    _UPLOAD_IMAGE_INPUT = "//input[@id='multipleupload-wall']"
    _PRIVACY_SETTINGS_BUTTON = "//div[@class='ossn-wall-privacy']"

    _SAVE_PRIVACY_SETTINGS_BUTTON = "//a[text()='Save']"
    _POST_BUTTON = "//input[@value='Post']"

    # Radios
    _RADIO_PRIVATE_PUBLIC_STATUS = "(//input[@class='ossn-radio-input'])[1]"
    _RADIO_PRIVATE_FRIENDS_STATUS = "(//input[@class='ossn-radio-input'])[2]"

    TAG_FRIEND_BY_NAME = lambda self, name: ("xpath", f"//div[@class='token-input-dropdown']//li//img[@title='{name}']")

    @allure.step("Write post")
    def write_post(self, text: str):
        self.ui.fill(self._POST_TEXTAREA, text)
        self.ui.screenshot()

    @allure.step("Tag friend")
    def tag_friends(self, friends: str | list):
        """
        Этот метод тэггирует друзей.
        :param friends: Полное имя друга или список полных имён.
        :return: None
        """
        if isinstance(friends, str):
            friends = [friends]

        for friend in friends:
            self.ui.click(self._TAG_FRIEND_BUTTON, "Tag friend")
            self.ui.fill(self._TAG_FRIEND_FIELD, friend)
            locator = self.TAG_FRIEND_BY_NAME(friend)
            self.ui.find(locator, wait=True).click()

    @allure.step("Choose post visibility status")
    def set_visibility_status(self, status: str):
        """
        This method accepts post visibility status
        :param status: public/friends
        :return: None
        """
        self.ui.find(self._PRIVACY_SETTINGS_BUTTON, True).click()

        if status == "public":
            self.ui.find(self._RADIO_PRIVATE_PUBLIC_STATUS, True).click()
            radio_status = self.ui.find(self._RADIO_PRIVATE_PUBLIC_STATUS)
            if radio_status.is_selected():
                self.ui.click(self._SAVE_PRIVACY_SETTINGS_BUTTON, "Save button")

        elif status == "friends":
            self.ui.find(self._RADIO_PRIVATE_FRIENDS_STATUS, True).click()
            radio_status = self.ui.find(self._RADIO_PRIVATE_FRIENDS_STATUS)
            if radio_status.is_selected():
                self.ui.click(self._SAVE_PRIVACY_SETTINGS_BUTTON, "Save button")

    @allure.step("Upload image")
    def upload_image(self, source: str):
        self.ui.find(self._ADD_IMAGE_BUTTON, wait=True).click()
        self.ui.fill(self._UPLOAD_IMAGE_INPUT, source)
        self.ui.screenshot()

    @allure.step("Post")
    def publish(self):
        self.ui.find(self._POST_BUTTON, True).click()
