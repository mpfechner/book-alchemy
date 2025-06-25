import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"
app.config["SECRET_KEY"] = "this-is-my-secret-key"
db.init_app(app)


@app.route("/")
def index():
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get("name")
        birth_date = request.form.get("birthdate")  # ✅ aus dem HTML übernommen
        date_of_death = request.form.get("date_of_death")

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
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        publication_year = request.form.get("publication_year")
        author_id = request.form.get("author_id")

        if not title or not isbn or not author_id:
            flash("Missing required fields!", "error")
            return redirect(url_for("add_book"))

        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=int(author_id)
        )
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for("add_book"))

    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


if __name__ == "__main__":
    with app.app_context():
        #db.create_all()
        app.run(debug=True, port=5002)
