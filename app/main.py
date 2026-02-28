import os
import sys
import json
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from app.services import UserService, VideoService

app = FastAPI(title="Python Video Hosting", version="0.1.0")

video_service = VideoService()
user_service = UserService()


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
