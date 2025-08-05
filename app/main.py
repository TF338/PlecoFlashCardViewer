import logging
from pathlib import Path

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from app.database.database import init_db
from app.dependencies.dependency import get_service_container
from app.dependencies.service_container import ServiceContainer
from dotenv import load_dotenv
import os

import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/app/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

load_dotenv()
port = int(os.getenv("PORT", 8000))
host = os.getenv("HOST", "127.0.0.1")

@app.on_event("startup")
async def on_startup():
    initialize_application()
    
@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    services: ServiceContainer = Depends(get_service_container),
):
    categories = services.category_repository.get_all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "categories": categories,
        "cards": [],
        "selected_category": None,
        "max_score": ""
    })


@app.post("/", response_class=HTMLResponse)
async def filter_cards(
        request: Request,
        category_id: int = Form(...),
        max_score: int = Form(...),
        services: ServiceContainer = Depends(get_service_container),
):
    categories = services.category_repository.get_all()
    cards = services.flashcard_repository.get_by_category_and_score(category_id, max_score)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "categories": categories,
        "cards": cards,
        "selected_category": category_id,
        "max_score": max_score
    })

def initialize_application():
    """Main application initialization routine"""
    try:
        logger.info("Starting database initialization...")
        init_db(create_tables=True)
        logger.info("Application initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Application initialization failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    if initialize_application():
        logger.info("Running application...")
        uvicorn.run("app.main:app", host=host, port=port, reload=True)
    else:
        logger.error("Application cannot start due to initialization errors")
        exit(1)
