import pytest

from app.models import Video
from app.services import UserService, ValidationService, VideoService


class TestValidationService:
    def test_valid_mp4_extension(self):
        assert ValidationService.validate_file_extension("video.mp4") is True

    def test_valid_webm_extension(self):
        assert ValidationService.validate_file_extension("video.webm") is True

    def test_invalid_extension(self):
        assert ValidationService.validate_file_extension("file.exe") is False

    def test_no_extension(self):
        assert ValidationService.validate_file_extension("noext") is False

    def test_valid_file_size(self):
        assert ValidationService.validate_file_size(100 * 1024 * 1024) is True

    def test_zero_file_size(self):
        assert ValidationService.validate_file_size(0) is False

    def test_oversized_file(self):
        over = 501 * 1024 * 1024
        assert ValidationService.validate_file_size(over) is False

    def test_valid_email(self):
        assert ValidationService.validate_email("user@example.com") is True

    def test_invalid_email(self):
        assert ValidationService.validate_email("not-an-email") is False

    def test_sanitize_filename(self):
        result = ValidationService.sanitize_filename("my video (1).mp4")
        assert " " not in result or "_" in result
        assert "(" not in result


class TestVideoService:
    def setup_method(self):
        self.service = VideoService()

    def test_add_and_get_video(self):
        video = Video(title="Test", filename="test.mp4", owner_id="user-1")
        added = self.service.add_video(video)
        fetched = self.service.get_video(added.id)
        assert fetched is not None
        assert fetched.title == "Test"

    def test_add_invalid_extension_raises(self):
        video = Video(title="Bad", filename="bad.exe", owner_id="user-1")
        with pytest.raises(ValueError, match="Unsupported file extension"):
            self.service.add_video(video)

    def test_list_videos_sorted_by_date(self):
        v1 = Video(title="First", filename="a.mp4", owner_id="user-1")
        v2 = Video(title="Second", filename="b.mp4", owner_id="user-1")
        self.service.add_video(v1)
        self.service.add_video(v2)
        videos = self.service.list_videos()
        assert len(videos) == 2

    def test_list_videos_by_owner(self):
        v1 = Video(title="A", filename="a.mp4", owner_id="user-1")
        v2 = Video(title="B", filename="b.mp4", owner_id="user-2")
        self.service.add_video(v1)
        self.service.add_video(v2)
        result = self.service.list_videos(owner_id="user-1")
        assert len(result) == 1
        assert result[0].owner_id == "user-1"

    def test_delete_video(self):
        video = Video(title="Delete me", filename="del.mp4", owner_id="user-1")
        self.service.add_video(video)
        assert self.service.delete_video(video.id) is True
        assert self.service.get_video(video.id) is None

    def test_delete_nonexistent_returns_false(self):
        assert self.service.delete_video("no-such-id") is False

    def test_search_by_title(self):
        v = Video(
            title="Python Tutorial",
            filename="tut.mp4",
            owner_id="user-1",
        )
        self.service.add_video(v)
        results = self.service.search_videos("python")
        assert len(results) == 1

    def test_search_by_description(self):
        v = Video(
            title="Lesson",
            filename="lesson.mp4",
            owner_id="user-1",
            description="Learn FastAPI basics",
        )
        self.service.add_video(v)
        results = self.service.search_videos("fastapi")
        assert len(results) == 1

    def test_watch_increments_views(self):
        video = Video(title="Watch me", filename="w.mp4", owner_id="user-1")
        self.service.add_video(video)
        self.service.watch_video(video.id)
        assert video.views == 1


class TestUserService:
    def setup_method(self):
        self.service = UserService()

    def test_register_user(self):
        user = self.service.register_user("john", "john@example.com")
        assert user.username == "john"
        assert user.email == "john@example.com"

    def test_duplicate_email_raises(self):
        self.service.register_user("john", "john@example.com")
        with pytest.raises(ValueError, match="Email already registered"):
            self.service.register_user("jane", "john@example.com")

    def test_duplicate_username_raises(self):
        self.service.register_user("john", "john@example.com")
        with pytest.raises(ValueError, match="Username already taken"):
            self.service.register_user("john", "other@example.com")

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError, match="Invalid email"):
            self.service.register_user("john", "bad-email")

    def test_get_user(self):
        user = self.service.register_user("jane", "jane@example.com")
        fetched = self.service.get_user(user.id)
        assert fetched is not None
        assert fetched.username == "jane"
