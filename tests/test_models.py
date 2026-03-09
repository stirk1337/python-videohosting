import pytest

from app.models import User, Video


class TestUser:
    def test_create_valid_user(self):
        user = User(username="testuser", email="test@example.com")
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.id is not None

    def test_username_stripped(self):
        user = User(username="  testuser  ", email="test@example.com")
        assert user.username == "testuser"

    def test_email_lowered(self):
        user = User(username="testuser", email="Test@Example.COM")
        assert user.email == "test@example.com"

    def test_empty_username_raises(self):
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User(username="", email="test@example.com")

    def test_whitespace_username_raises(self):
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User(username="   ", email="test@example.com")

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError, match="Invalid email"):
            User(username="testuser", email="not-an-email")


class TestVideo:
    def test_create_valid_video(self):
        video = Video(title="My Video", filename="clip.mp4", owner_id="user-123")
        assert video.title == "My Video"
        assert video.filename == "clip.mp4"
        assert video.views == 0

    def test_empty_title_raises(self):
        with pytest.raises(ValueError, match="Video title cannot be empty"):
            Video(title="", filename="clip.mp4", owner_id="user-123")

    def test_empty_filename_raises(self):
        with pytest.raises(ValueError, match="Filename cannot be empty"):
            Video(title="My Video", filename="", owner_id="user-123")

    def test_increment_views(self):
        video = Video(title="My Video", filename="clip.mp4", owner_id="user-123")
        assert video.views == 0
        video.increment_views()
        assert video.views == 1
        video.increment_views()
        assert video.views == 2

    def test_extension_property(self):
        video = Video(title="My Video", filename="clip.mp4", owner_id="user-123")
        assert video.extension == "mp4"

    def test_extension_no_dot(self):
        video = Video(title="My Video", filename="noextension", owner_id="user-123")
        assert video.extension == ""
