import os
import re
from typing import Optional

from app.config import Config
from app.models import User, Video


class ValidationService:
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        if "." not in filename:
            return False
        ext = filename.rsplit(".", 1)[-1].lower()
        return ext in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def validate_file_size(size_bytes: int) -> bool:
        max_bytes = Config.MAX_VIDEO_SIZE_MB * 1024 * 1024
        return 0 < size_bytes <= max_bytes

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        name = re.sub(r"[^\w\s\-.]", "", filename)
        name = re.sub(r"\s+", "_", name)
        return name


class VideoService:
    def __init__(self):
        self._videos: dict[str, Video] = {}

    def add_video(self, video: Video) -> Video:
        if not ValidationService.validate_file_extension(video.filename):
            raise ValueError(
                f"Unsupported file extension: {video.extension}. "
                f"Allowed: {Config.ALLOWED_EXTENSIONS}"
            )
        self._videos[video.id] = video
        return video

    def get_video(self, video_id: str) -> Optional[Video]:
        return self._videos.get(video_id)

    def list_videos(self, owner_id: Optional[str] = None) -> list[Video]:
        videos = list(self._videos.values())
        if owner_id:
            videos = [v for v in videos if v.owner_id == owner_id]
        return sorted(videos, key=lambda v: v.created_at, reverse=True)

    def delete_video(self, video_id: str) -> bool:
        if video_id in self._videos:
            del self._videos[video_id]
            return True
        return False

    def search_videos(self, query: str) -> list[Video]:
        query_lower = query.lower()
        return [
            v
            for v in self._videos.values()
            if query_lower in v.title.lower() or query_lower in v.description.lower()
        ]

    def watch_video(self, video_id: str) -> Optional[Video]:
        video = self.get_video(video_id)
        if video:
            video.increment_views()
        return video


class UserService:
    def __init__(self):
        self._users: dict[str, User] = {}

    def register_user(self, username: str, email: str) -> User:
        if not ValidationService.validate_email(email):
            raise ValueError(f"Invalid email: {email}")

        for user in self._users.values():
            if user.email == email.strip().lower():
                raise ValueError(f"Email already registered: {email}")
            if user.username == username.strip():
                raise ValueError(f"Username already taken: {username}")

        user = User(username=username, email=email)
        self._users[user.id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_upload_path(self, user_id: str) -> str:
        return os.path.join(Config.UPLOAD_DIR, user_id)
