from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    Author model with optional birth and death dates.
    """
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String, nullable=False)
    birth_date: str = db.Column(db.String, nullable=True)
    date_of_death: str = db.Column(db.String, nullable=True)

    def __repr__(self) -> str:
        return f"<Author {self.name}>"

    def __str__(self) -> str:
        return self.name


class Book(db.Model):
    """
    Book model including basic metadata and a relationship to an author.
    """
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn: str = db.Column(db.String, nullable=False)
    title: str = db.Column(db.String, nullable=False)
    publication_year: str = db.Column(db.String, nullable=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    rating: int = db.Column(db.Integer, nullable=True)  # 1–10 scale (optional)

    # Establish relationship with Author
    author: Author = db.relationship("Author", backref="books")

    def __repr__(self) -> str:
        return f"<Book {self.title}>"

    def __str__(self) -> str:
        return self.title
