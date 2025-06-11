import os
import time
import pytest
import allure
from faker import Faker
from base.base_test import BaseTest
from pages.new_business_page.page import BusinessPageBuilder

faker = Faker()

@allure.epic("News Feed")
@allure.feature("Posts")
class TestNewsFeed(BaseTest):

    @pytest.mark.smoke
    @allure.title("Create new post")
    @pytest.mark.parametrize("add_users", [1], indirect=True)
    @pytest.mark.parametrize("message, visibility", [
        ("Hello 123", "public"),
        ("Hello", "friends"),
    ])
    def test_create_new_post(self, add_users, message, visibility):
        friend = add_users[0]

        # Admin actions
        self.login_page().open()
        self.login_page().login_as("admin")
        self.sidebar().links.open_news_feed()
        self.news_feed_page().post_form.write_post(message)
        self.news_feed_page().post_form.tag_friends("Keon Daniel")
        self.news_feed_page().post_form.upload_image(f"{os.getcwd()}/temp_files/my_picture.png")
        self.news_feed_page().post_form.set_visibility_status(visibility)
        self.news_feed_page().post_form.publish()

        # Friends actions
        self.login_page(friend).open()
        self.login_page(friend).login_as("friend")
        self.sidebar(friend).links.open_news_feed()
        self.news_feed_page(friend).is_post_published(message, visibility)

    @pytest.mark.smoke
    @allure.title("Create new business page")
    def test_create_new_business_page(self):
        self.login_page().open()
        self.login_page().login_as("friend")
        self.sidebar().business_page.create_new_business_page()
        self.new_business_page().page_builder.set_page_name("QWE")
        self.new_business_page().fill_required()
        self.new_business_page().is_page_created()

    @pytest.mark.smoke
    @allure.title("Send a message")
    @pytest.mark.parametrize("add_users", [1], indirect=True)
    def test_send_message(self, add_users):
        admin = add_users[0]
        self.login_page().open()
        self.login_page().login_as("friend")
        self.sidebar().links.open_messages()
        self.messages_page().choose_thread("Admin", "Admin")
        message = faker.word()
        self.messages_page().send_message(message)
        self.messages_page().is_message_sent(message)

        # Admin actions
        self.login_page(admin).open()
        self.login_page(admin).login_as("admin")
        self.news_feed_page(admin).is_new_messages()
        self.news_feed_page(admin).check_message_sender("Keon Daniel")





