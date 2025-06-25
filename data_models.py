from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String, nullable=True)
    date_of_death = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return self.name

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.String, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    author = db.relationship("Author", backref="books")

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return self.title
