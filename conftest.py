from fixtures.ui_fixtures import *
from fixtures.api_fixtures import *
import requests  # библиотека для HTTP-запросов
import pytest  # фреймворк для тестирования
import datetime  # модуль для работы с датой и временем

CHAT_ID_TELEGRAM = "-4986897412" # ID чата в Telegram, куда будут отправляться результаты
TOKEN_TELEGRAM = "7561480034:AAH3VWBNLWdpUn-q5HJGHop9y0VPtBvwSBA" # Токен бота Telegram, который будет отправлять сообщения
GITHUB_PAGES_URL = "https://timtestqa.github.io/web_ui_tests/" # URL API GitLab для получения файла с результатами тестов


def pytest_terminal_summary(terminalreporter):
    """
    Хук pytest, выполняющийся после завершения всех тестов.
    Собирает статистику по результатам и отправляет сводку в Telegram.
    """
    config = terminalreporter.config
    if hasattr(config, "workerinput"):
        return

    # Фиксируем время запуска сборки
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Структура для хранения агрегированных результатов по каждому файлу тестов
    suite_results = {}

    # Проходим по всем результатам, которые pytest сохранил в terminalreporter.stats
    for outcome, reports in terminalreporter.stats.items():
        for report in reports:
            # Получаем только имя файла без пути и расширения
            suite_name = report.nodeid.split("::")[0].split("/")[-1].replace(".py", "")
            
            # Пропускаем пустые имена файлов
            if not suite_name:
                continue

            # Если встретился новый файл тестов, инициализируем для него счётчики
            if suite_name not in suite_results:
                suite_results[suite_name] = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0}

            # Увеличиваем соответствующий счётчик
            if outcome == "passed":
                suite_results[suite_name]["passed"] += 1
            elif outcome == "failed":
                suite_results[suite_name]["failed"] += 1
            elif outcome == "skipped":
                suite_results[suite_name]["skipped"] += 1
            elif outcome == "error":
                suite_results[suite_name]["errors"] += 1

    # Формируем текст сообщения для Telegram
    message = f"*РЕЗУЛЬТАТЫ ТЕСТОВ:*\n*Время запуска:* {start_time}\n\n"

    for suite, results in suite_results.items():
        # Пропускаем сьюты без результатов
        if all(count == 0 for count in results.values()):
            continue
            
        message += (
            f"*Сьют:* `{suite}`\n\n"
            f"✅ *Пройдено:* {results['passed']}\n\n"
            f"❌ *Не пройдено:* {results['failed']}\n\n"
            f"⏭ *Пропущено:* {results['skipped']}\n\n"
            f"⚠️ *Ошибки:* {results['errors']}\n\n"
            f"-----------------------------\n\n"
        )

    # Добавляем ссылку на GitLab
    message += f"[Подробнее на GitLab Pages]({GITLAB_URL})"

    try:
        # Отправляем POST-запрос к Telegram Bot API
        response = requests.post(
            url=f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            headers={"Content-Type": "application/json"},
            json={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
        )
        # Проверяем, нет ли ошибок в ответе
        response.raise_for_status()
    except requests.RequestException as e:
        # Если запрос не удался, выводим содержимое ответа для отладки
        if e.response is not None:
            print("Ответ Телеграмма:", e.response.json())
        print(f"Ошибка при отправке сообщения в Telegram: {e}")