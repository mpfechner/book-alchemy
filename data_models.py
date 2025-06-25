from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Author(db.Model):
    """
    Author model with optional birth and death dates.
    """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[str] = mapped_column(nullable=True)
    date_of_death: Mapped[str] = mapped_column(nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")

    def __repr__(self) -> str:
        return f"<Author {self.name}>"

    def __str__(self) -> str:
        return self.name


class Book(db.Model):
    """
    Book model including basic metadata and a relationship to an author.
    """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    publication_year: Mapped[str] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(db.ForeignKey("author.id"), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=True)  # 1–10 scale (optional)

    author: Mapped["Author"] = relationship("Author", back_populates="books")

    def __repr__(self) -> str:
        return f"<Book {self.title}>"

    def __str__(self) -> str:
        return self.title
