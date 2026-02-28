from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class User:
    username: str
    email: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not self.username or not self.username.strip():
            raise ValueError("Username cannot be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email address")
        self.username = self.username.strip()
        self.email = self.email.strip().lower()


@dataclass
class Video:
    title: str
    filename: str
    owner_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    duration_seconds: Optional[int] = None
    views: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Video title cannot be empty")
        if not self.filename:
            raise ValueError("Filename cannot be empty")
        self.title = self.title.strip()

    def increment_views(self):
        self.views += 1

    @property
    def extension(self) -> str:
        return self.filename.rsplit(".", 1)[-1].lower() if "." in self.filename else ""
