import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///videohosting.db")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    MAX_VIDEO_SIZE_MB = int(os.getenv("MAX_VIDEO_SIZE_MB", "500"))
    ALLOWED_EXTENSIONS = {"mp4", "webm", "mkv", "avi", "mov"}
