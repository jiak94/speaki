import os

AZURE_KEY = os.getenv("AZURE_KEY", "")
AZURE_REGION = os.getenv("AZURE_REGION", "")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "speaki")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

MEDIA_PATH = os.getenv("MEDIA_PATH", "/media")