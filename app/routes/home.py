from fastapi import APIRouter, Request
from app.templates_config import templates
from app.routes.blog import get_posts

router = APIRouter()


@router.get("/")
async def home(request: Request):
    featured = get_posts()[:3]
    return templates.TemplateResponse(request, "index.html", {"featured": featured})


@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html")
