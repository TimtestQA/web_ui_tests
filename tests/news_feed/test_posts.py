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
        self.login_page().screenshot("login_page_opened")
        
        self.login_page().login_as("admin")
        self.login_page().screenshot("admin_logged_in")
        
        self.sidebar().links.open_news_feed()
        self.sidebar().screenshot("news_feed_opened")
        
        self.news_feed_page().post_form.write_post(message)
        self.news_feed_page().post_form.tag_friends("Keon Daniel")
        self.news_feed_page().post_form.upload_image(f"{os.getcwd()}/temp_files/my_picture.png")
        self.news_feed_page().post_form.set_visibility_status(visibility)
        self.news_feed_page().post_form.publish()
        self.news_feed_page().screenshot("post_published")

        # Friends actions
        self.login_page(friend).open()
        self.login_page(friend).screenshot("friend_login_page_opened")
        
        self.login_page(friend).login_as("friend")
        self.login_page(friend).screenshot("friend_logged_in")
        
        self.sidebar(friend).links.open_news_feed()
        self.sidebar(friend).screenshot("friend_news_feed_opened")
        
        self.news_feed_page(friend).is_post_published(message, visibility)
        self.news_feed_page(friend).screenshot("post_verified_by_friend")

    @pytest.mark.negative_posts
    @allure.title("Create post with invalid data")
    @pytest.mark.parametrize("message, visibility, error_message", [
        ("", "public", "This value is required"),
        (" ", "public", "This value is required"),
        ("a" * 1001, "public", "This value is too long"),
        ("<script>alert('xss')</script>", "public", "Invalid characters detected"),
        ("' OR '1'='1", "public", "Invalid characters detected"),
        ("Hello", "invalid_visibility", "Invalid visibility option"),
    ])
    def test_create_post_with_invalid_data(self, message, visibility, error_message):
        self.login_page().open()
        self.login_page().login_as("admin")
        self.sidebar().links.open_news_feed()
        
        self.news_feed_page().post_form.write_post(message)
        self.news_feed_page().post_form.set_visibility_status(visibility)
        self.news_feed_page().post_form.publish()
        
        assert self.news_feed_page().post_form.get_error_message() == error_message

    @pytest.mark.negative_posts
    @allure.title("Create post with invalid image")
    @pytest.mark.parametrize("image_path, error_message", [
        ("invalid_path.png", "File not found"),
        ("temp_files/invalid_extension.txt", "Invalid file type"),
        ("temp_files/too_large.jpg", "File size exceeds limit"),
    ])
    def test_create_post_with_invalid_image(self, image_path, error_message):
        self.login_page().open()
        self.login_page().login_as("admin")
        self.sidebar().links.open_news_feed()
        
        self.news_feed_page().post_form.write_post("Test post")
        self.news_feed_page().post_form.upload_image(f"{os.getcwd()}/{image_path}")
        self.news_feed_page().post_form.publish()
        
        assert self.news_feed_page().post_form.get_error_message() == error_message

    @pytest.mark.smoke
    @allure.title("Create new business page")
    def test_create_new_business_page(self):
        self.login_page().open()
        self.login_page().screenshot("login_page_opened")
        
        self.login_page().login_as("friend")
        self.login_page().screenshot("friend_logged_in")
        
        self.sidebar().business_page.create_new_business_page()
        self.sidebar().screenshot("business_page_creation_started")
        
        self.new_business_page().page_builder.set_page_name("QWE")
        self.new_business_page().fill_required()
        self.new_business_page().screenshot("business_page_data_filled")
        
        self.new_business_page().is_page_created()
        self.new_business_page().screenshot("business_page_created")

    @pytest.mark.negative_business
    @allure.title("Create business page with invalid data")
    @pytest.mark.parametrize("page_name, error_message", [
        ("", "This value is required"),
        (" ", "This value is required"),
        ("a" * 101, "This value is too long"),
        ("<script>alert('xss')</script>", "Invalid characters detected"),
        ("' OR '1'='1", "Invalid characters detected"),
    ])
    def test_create_business_page_with_invalid_data(self, page_name, error_message):
        self.login_page().open()
        self.login_page().login_as("friend")
        self.sidebar().business_page.create_new_business_page()
        
        self.new_business_page().page_builder.set_page_name(page_name)
        self.new_business_page().fill_required()
        
        assert self.new_business_page().page_builder.get_error_message() == error_message

    @pytest.mark.smoke
    @allure.title("Send a message")
    @pytest.mark.parametrize("add_users", [1], indirect=True)
    def test_send_message(self, add_users):
        admin = add_users[0]
        
        self.login_page().open()
        self.login_page().screenshot("login_page_opened")
        
        self.login_page().login_as("friend")
        self.login_page().screenshot("friend_logged_in")
        
        self.sidebar().links.open_messages()
        self.sidebar().screenshot("messages_page_opened")
        
        self.messages_page().choose_thread("Admin", "Admin")
        message = faker.word()
        self.messages_page().send_message(message)
        self.messages_page().screenshot("message_sent")
        
        self.messages_page().is_message_sent(message)
        self.messages_page().screenshot("message_verified")

        # Admin actions
        self.login_page(admin).open()
        self.login_page(admin).screenshot("admin_login_page_opened")
        
        self.login_page(admin).login_as("admin")
        self.login_page(admin).screenshot("admin_logged_in")
        
        self.news_feed_page(admin).is_new_messages()
        self.news_feed_page(admin).screenshot("new_messages_notification")
        
        self.news_feed_page(admin).check_message_sender("Keon Daniel")
        self.news_feed_page(admin).screenshot("message_sender_verified")

    @pytest.mark.negative_messages
    @allure.title("Send message with invalid data")
    @pytest.mark.parametrize("message, error_message", [
        ("", "This value is required"),
        (" ", "This value is required"),
        ("a" * 1001, "This value is too long"),
        ("<script>alert('xss')</script>", "Invalid characters detected"),
        ("' OR '1'='1", "Invalid characters detected"),
    ])
    def test_send_message_with_invalid_data(self, message, error_message):
        self.login_page().open()
        self.login_page().login_as("friend")
        self.sidebar().links.open_messages()
        
        self.messages_page().choose_thread("Admin", "Admin")
        self.messages_page().send_message(message)
        
        assert self.messages_page().get_error_message() == error_message





