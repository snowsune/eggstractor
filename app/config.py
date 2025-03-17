import os


class Config:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "/app/downloads")


config = Config()
