from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.metrics import VIDEO_VIEWS_TOTAL, setup_metrics
from app.services import UserService, VideoService

app = FastAPI(title="Python Video Hosting", version="0.1.0")

video_service = VideoService()
user_service = UserService()

setup_metrics(app)


class RegisterRequest(BaseModel):
    username: str
    email: str


class VideoUploadRequest(BaseModel):
    title: str
    description: str = ""
    owner_id: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/users/register")
def register_user(request: RegisterRequest):
    try:
        user = user_service.register_user(request.username, request.email)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/videos")
def list_videos(owner_id: str | None = None):
    videos = video_service.list_videos(owner_id)
    return [
        {
            "id": v.id,
            "title": v.title,
            "views": v.views,
            "created_at": v.created_at.isoformat(),
        }
        for v in videos
    ]


@app.get("/videos/{video_id}")
def get_video(video_id: str):
    video = video_service.watch_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    VIDEO_VIEWS_TOTAL.inc()
    return {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "views": video.views,
        "filename": video.filename,
    }


@app.get("/videos/search/{query}")
def search_videos(query: str):
    results = video_service.search_videos(query)
    return [{"id": v.id, "title": v.title, "views": v.views} for v in results]


@app.post("/api/fail")
def incident_simulate_failure():
    """Simulate high 5xx rate for monitoring drills (Practice 206)."""
    raise HTTPException(
        status_code=500,
        detail="Simulated failure for observability drill",
    )
