import uuid

from flask import Flask, redirect, render_template, request, url_for
from replit import db

app = Flask(__name__)


def get_books():
    return {key: db[key] for key in db if key.startswith("book-")}


@app.route("/")
def index():
    books = get_books()
    return render_template("index.html", books=books)


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")
    description = request.form.get("description")

    if title and author:  # Перевірка, що обов'язкові поля заповнені
        book_id = f"book-{uuid.uuid4().hex}"  # Унікальний ідентифікатор
        db[book_id] = {
            "title": title,
            "author": author,
            "description": description
        }

    return redirect(url_for("index"))


@app.route("/delete/<book_id>")
def delete_book(book_id):
    key = f"book-{book_id}"
    if key in db:  # Перевірка існування ключа
        del db[key]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
