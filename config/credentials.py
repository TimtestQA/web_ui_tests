import os

from dotenv import load_dotenv

print("Checking .env file:", os.path.exists('.env'))
load_dotenv()

class Credentials:
    # Debug print
    print("Current working directory:", os.getcwd())
    print("Files in current directory:", os.listdir())
    print("TG_BOT_TOKEN:", os.getenv("TG_BOT_TOKEN"))
    print("TG_CHAT_ID:", os.getenv("TG_CHAT_ID"))
    print("GITHUB_PAGES_URL:", os.getenv("GITHUB_PAGES_URL"))

    # FakeWorld123
    FRIEND_LOGIN = os.getenv("FRIEND_LOGIN")
    FRIEND_PASSWORD = os.getenv("FRIEND_PASSWORD")

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    # Bot settings
    BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    BOT_ID = os.getenv("TG_CHAT_ID")
    PAGES_URL = os.getenv("GITHUB_PAGES_URL")