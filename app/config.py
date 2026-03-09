import os


class Config:
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")  # nosec B104 — needed for Docker
    APP_PORT = int(os.getenv("APP_PORT", "8000"))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///videohosting.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://cache:6379/0")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    MAX_VIDEO_SIZE_MB = int(os.getenv("MAX_VIDEO_SIZE_MB", "500"))
    ALLOWED_EXTENSIONS = {"mp4", "webm", "mkv", "avi", "mov"}
