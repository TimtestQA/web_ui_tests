import time
from asyncio import timeout

import allure
from base.base_page import BasePage
from config.links import Links


class MessagesPage(BasePage):

    _PAGE_URL = Links.MESSAGE_PAGE

    _MESSAGE_AREA = "//textarea[@name='message']"
    _SEND_BUTTON = "//input[@type='submit']"
    _MESSAGE_ROWS = "//div[contains(@class, 'message-box-sent')]//span"

    @allure.step("Choose thread")
    def choose_thread(self, first_name, last_name):
        locator = ("xpath", f"//div[@class='name' and text()='{first_name} {last_name}']")
        self.ui.click(locator)

    @allure.step("Send message")
    def send_message(self, message):
        self.ui.fill(self._MESSAGE_AREA, message)
        self.ui.click(self._SEND_BUTTON)

    @allure.step("Check if message is sent")
    def is_message_sent(self, message):
        timeout = 10  # Максимальное время ожидания
        last_message = None

        # Начальная проверка
        all_messages = self.ui.find_all(self._MESSAGE_ROWS)
        initial_count = len(all_messages)

        # Ожидаем, пока количество сообщений увеличится
        while len(all_messages) == initial_count:
            time.sleep(1)
            all_messages = self.ui.find_all(self._MESSAGE_ROWS)
            timeout -= 1
            if timeout == 0:
                raise TimeoutError(f"Message '{message}' was not sent in time.")

        # Получаем последнее сообщение
        last_message = all_messages[-1]

        # Ожидаем появления текста в новом сообщении
        self.ui.wait_for_text_in_web_element(last_message, message)

        # Печатаем текст сообщения
        print(last_message.text)

