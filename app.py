import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"
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



if __name__ == "__main__":
    with app.app_context():
        #db.create_all()
        app.run(debug=True, port=5002)
