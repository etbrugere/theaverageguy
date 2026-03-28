from fastapi import APIRouter, Request, HTTPException
from app.templates_config import templates
from pathlib import Path
import frontmatter
import markdown as md

router = APIRouter()

POSTS_DIR = Path(__file__).parent.parent / "content" / "posts"


def get_posts() -> list[dict]:
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        post = frontmatter.load(path)
        posts.append({
            "slug": path.stem,
            "title": post.get("title", "Sans titre"),
            "date": str(post.get("date", "")),
            "category": post.get("category", ""),
            "excerpt": post.get("excerpt", ""),
            "cover": post.get("cover", ""),
        })
    return posts


@router.get("/blog")
async def blog_list(request: Request):
    posts = get_posts()
    return templates.TemplateResponse(request, "blog.html", {"posts": posts})


@router.get("/blog/{slug}")
async def blog_post(request: Request, slug: str):
    path = POSTS_DIR / f"{slug}.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Article introuvable")
    post = frontmatter.load(path)
    content = md.markdown(post.content, extensions=["extra", "tables", "fenced_code"])
    return templates.TemplateResponse(request, "article.html", {
        "title": post.get("title", ""),
        "date": str(post.get("date", "")),
        "category": post.get("category", ""),
        "excerpt": post.get("excerpt", ""),
        "content": content,
    })
