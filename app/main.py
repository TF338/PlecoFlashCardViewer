import logging
from pathlib import Path

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import init_db, get_session
from app.repository.category_repository import CategoryRepository
from app.repository.flash_card_respository import FlashCardRepository
from dotenv import load_dotenv
import os

import uvicorn

# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# === FastAPI App & Templates ===
app = FastAPI()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

load_dotenv()
port = int(os.getenv("PORT", 8000))
host = os.getenv("HOST", "127.0.0.1")

# === Routes ===

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, session=Depends(get_session)):
    categories = CategoryRepository(session).get_all()
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
    session: Session = Depends(get_session)
):
    categories = CategoryRepository(session).get_all()
    cards = FlashCardRepository(session).get_by_category_and_score(category_id, max_score)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "categories": categories,
        "cards": cards,
        "selected_category": category_id,
        "max_score": max_score
    })

# === Initialization ===

def initialize_application():
    """Main application initialization routine"""
    try:
        logger.info("Starting database initialization...")

        # Initialize database (will use latest .pqb backup if available)
        init_db(create_tables=True)

        logger.info("Application initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Application initialization failed: {str(e)}", exc_info=True)
        return False


# === Entry Point ===
if __name__ == "__main__":
    if initialize_application():
        logger.info("Running application...")
        uvicorn.run("app.main:app", host=host, port=port, reload=True)
    else:
        logger.error("Application cannot start due to initialization errors")
        exit(1)
