"""
Book Service.
"""
from typing import List

from sqlalchemy.exc import IntegrityError, InvalidRequestError, OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app import entities
from app.config import Config
from app.db.models import Books as BookModel
from app.exceptions import EntityNotFoundException, InvalidInputException
from app.logger import logger
from app.utils import random_resource_id


class BookService:
    def __init__(self, config: Config) -> None:
        """Init

        Args:
            config (Config): configurations. Parameters are set from env vars.
        """
        self.config = config
        self.logger = logger

    def create_book(self, db: Session, entry: entities.BookCreate) -> BookModel:
        """Create new book entry.

        Args:
            db (Session): DB
            entry (entities.BookCreate): Request body.

        Raises:
            InvalidInputException: Invalid input was specified.

        Returns:
            BookModel: Book entry.
        """
        try:
            book_id = random_resource_id()
            book_model = BookModel(book_id=book_id, title=entry.title)
            db.add(book_model)
            db.commit()
            db.refresh(book_model)
            return book_model
        except (IntegrityError, OperationalError) as e:
            self.logger.error(e)
            raise InvalidInputException("Invalid input error.")

    def list_books(self, db: Session, limit: int, offset: int) -> List[BookModel]:
        """Return list of books.

        Args:
            db (Session): DB
            limit (int): number of entries to return.
            offset (int): number of offset as pagination.

        Raises:
            InvalidInputException: Invalid input was specified.

        Returns:
            List[BookModel]: List of BookModel.
        """
        try:
            return db.query(BookModel).limit(limit).offset(offset).all()
        except (InvalidRequestError, ProgrammingError) as e:
            self.logger.error(e)
            raise InvalidInputException("Invalid input error.")

    def fetch_book(self, db: Session, book_id: str) -> BookModel:
        """Return book.

        Args:
            db (Session): DB
            book_id (str): Book ID.

        Raises:
            EntityNotFoundException: Entity was not found.
            InvalidInputException: Invalid input was specified.

        Returns:
            BookModel: Book entry.
        """
        try:
            book_model = db.query(BookModel).filter(BookModel.book_id == book_id).one_or_none()
            if book_model is None:
                message = f"Not found: book_id={book_id}"
                self.logger.error(message)
                raise EntityNotFoundException(message)
            return book_model
        except InvalidRequestError as e:
            self.logger.error(e)
            raise InvalidInputException("Invalid input error.")
