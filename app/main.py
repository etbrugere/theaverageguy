from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import home, blog

BASE_DIR = Path(__file__).parent

app = FastAPI(title="The Average Guy")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(home.router)
app.include_router(blog.router)
