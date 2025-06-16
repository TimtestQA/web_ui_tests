# UI Automation Testing Project

Проект автоматизации UI тестирования с использованием Python, Selenium, Pytest и Allure.

## Структура проекта

```
├── base/                      # Базовые классы и компоненты
│   ├── base_page.py          # Базовый класс для страниц
│   ├── base_test.py          # Базовый класс для тестов
│   └── base_components/      # Базовые компоненты (сайдбар и т.д.)
├── config/                    # Конфигурационные файлы
│   └── credentials.py        # Учетные данные и переменные окружения
├── helpers/                   # Вспомогательные функции
│   └── ui_helper.py          # Хелперы для UI тестов
├── pages/                     # Page Objects
│   ├── login_page/           # Страница логина
│   ├── news_feed_page/       # Страница новостей
│   ├── messages_page/        # Страница сообщений
│   ├── new_business_page/    # Страница создания бизнеса
│   └── connect_page/         # Страница Connect
├── tests/                     # Тесты
│   ├── test_login.py         # Тесты логина
│   └── test_connect.py       # Тесты Connect
├── .env                       # Файл с переменными окружения
├── .gitignore                # Игнорируемые файлы Git
├── conftest.py               # Фикстуры Pytest
├── Dockerfile                # Конфигурация Docker
├── docker-compose.yml        # Конфигурация Docker Compose
├── requirements.txt          # Зависимости Python
└── README.md                 # Документация проекта
```

## Требования

- Python 3.14+
- Chrome/Firefox
- Docker (опционально)

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл .env и заполните его:
```env
BROWSER=chrome
ADMIN_LOGIN=your_admin_login
ADMIN_PASSWORD=your_admin_password
FRIEND_LOGIN=your_friend_login
FRIEND_PASSWORD=your_friend_password
TG_BOT_TOKEN=your_telegram_bot_token
TG_CHAT_ID=your_telegram_chat_id
GH_PAGES_URL=your_github_pages_url
```

## Запуск тестов

### Локальный запуск

```bash
# Запуск всех тестов
pytest -sv --alluredir=allure-results

# Запуск тестов логина
pytest -sv --alluredir=allure-results -m login

# Запуск тестов Connect
pytest -sv --alluredir=allure-results -m connect
```

### Запуск через Docker

```bash
# Запуск всех тестов
docker compose up

# Запуск тестов логина
docker compose up login

# Запуск тестов Connect
docker compose up connect
```

## Генерация отчета Allure

```bash
# Генерация отчета
allure generate allure-results --clean -o allure-report

# Просмотр отчета
allure serve allure-results
```

## Особенности проекта

1. **Page Object Pattern**: Используется для лучшей организации кода и поддержки
2. **Allure отчеты**: Детальные отчеты о выполнении тестов
3. **Docker поддержка**: Возможность запуска тестов в контейнерах
4. **Telegram уведомления**: Отправка результатов тестов в Telegram
5. **GitHub Pages**: Хостинг отчетов Allure
6. **Мультибраузерность**: Поддержка Chrome и Firefox
7. **Headless режим**: Возможность запуска без GUI
8. **Скриншоты при падении**: Автоматическое создание скриншотов при ошибках

## CI/CD

Проект настроен для работы с:
- GitHub Actions
- CircleCI