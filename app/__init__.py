from fastapi import FastAPI
from .config import setup_db
from .routers import users_router, translations_router

def create_app() -> FastAPI:
    """Create and configure a new FastAPI application instance."""
    app = FastAPI()

    app.include_router(users_router, prefix="/users")
    app.include_router(translations_router, prefix="/translations")

    setup_db()

    return app
