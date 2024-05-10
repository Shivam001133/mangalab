from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.getenv('DEBUG')
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# celery settings
CELERY_BROKER = os.getenv("CELERY_BROKER", "redis://127.0.0.1:6379/0")
CELERY_BACKEND = os.getenv("CELERY_BACKEND", "redis://127.0.0.1:6379/0")

# Database
MYSQL_DB_NAME = os.getenv('MYSQL_DB_NAME')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB_HOST = os.getenv('MYSQL_DB_HOST')
MYSQL_DB_PORT = os.getenv('MYSQL_DB_PORT')

# Rebbtmq
RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
RABBITMQ_SERVICE = os.getenv('RABBITMQ_SERVICE', 'mangalab-rabbitmq')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5672)
RABBITMQ_DEFAULT_VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST')

# Selenium
SELENIUM_HOST = os.getenv('SELENIUM_HOST', 'localhost')