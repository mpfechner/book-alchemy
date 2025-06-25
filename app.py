import os
from flask import Flask, flash, redirect, render_template, request, url_for
from data_models import db, Author, Book

app = Flask(__name__)

# Configure database and secret key
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"
app.config['SECRET_KEY'] = "this-is-my-secret-key"
db.init_app(app)


@app.route("/", methods=["GET"])
def index() -> str:
    """
    Render the homepage with optional filtering and sorting of books.
    """
    search_query = request.args.get("q", "").strip()
    sort_by = request.args.get("sort", "title")

    query = Book.query.join(Author)

    if search_query:
        search = f"%{search_query}%"
        query = query.filter(Book.title.ilike(search))

    if sort_by == "author":
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()
    return render_template("home.html", books=books, search_query=search_query, sort_by=sort_by)


@app.route("/add_author", methods=["GET", "POST"])
def add_author() -> str:
    """
    Handle creation of a new author via form input.
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birth_date = request.form.get("birthdate") or None
        date_of_death = request.form.get("date_of_death") or None

        if not name:
            flash("Name is required!", "error")
            return redirect(url_for("add_author"))

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        flash("Author added successfully!", "success")
        return redirect(url_for("add_author"))

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book() -> str:
    """
    Handle creation of a new book via form input.
    """
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        isbn = request.form.get("isbn", "").strip()
        publication_year = request.form.get("publication_year") or None
        author_id = request.form.get("author_id")
        rating = request.form.get("rating")

        try:
            rating = int(rating) if rating else None
        except ValueError:
            rating = None

        if not title or not isbn or not author_id:
            flash("Missing required fields!", "error")
            return redirect(url_for("add_book"))

        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=int(author_id),
            rating=rating
        )
        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully!", "success")
        return redirect(url_for("add_book"))

    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id: int) -> str:
    """
    Delete a book and optionally its author if no books remain.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    if not author.books:
        db.session.delete(author)
        db.session.commit()
        flash(f"Book and author '{author.name}' deleted.", "success")
    else:
        flash(f"Book '{book.title}' deleted.", "success")

    return redirect(url_for("index"))


@app.route("/author/<int:author_id>/confirm_delete", methods=["GET"])
def confirm_delete_author(author_id: int) -> str:
    """
    Show a confirmation page before deleting an author.
    """
    author = Author.query.get_or_404(author_id)
    return render_template("confirm_delete_author.html", author=author)


@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id: int) -> str:
    """
    Delete an author and all their books.
    """
    author = Author.query.get_or_404(author_id)
    books = author.books

    for book in books:
        db.session.delete(book)

    db.session.delete(author)
    db.session.commit()

    flash(f"Author '{author.name}' and {len(books)} book(s) deleted.", "success")
    return redirect(url_for("index"))


@app.route("/book/<int:book_id>", methods=["GET"])
def book_detail(book_id: int) -> str:
    """
    Display detailed information about a book.
    """
    book = Book.query.get_or_404(book_id)
    return render_template("book_detail.html", book=book)


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, port=5002)
