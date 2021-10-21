"""
Entrypoint of API server.
"""
from app.apis.configure_app import configure_app
from app.config import Config
from app.services.book_service import BookService

config = Config.initialize_from_env()

app = configure_app(
    book_service=BookService(
        config=config,
    ),
)
