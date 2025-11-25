from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookstore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    reviews = db.relationship(
        "Review",
        backref="book",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Book {self.title!r}>"


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.id} for book {self.book_id}>"


def create_tables_and_seed():
    """Create DB tables and seed initial books if empty."""
    db.create_all()

    if Book.query.count() == 0:
        books = [
            Book(
                title="Clean Code",
                author="Robert C. Martin",
                description="A handbook of agile software craftsmanship.",
            ),
            Book(
                title="Fluent Python",
                author="Luciano Ramalho",
                description="Clear, practical guidance for Python developers.",
            ),
            Book(
                title="Deep Learning",
                author="Ian Goodfellow, Yoshua Bengio, Aaron Courville",
                description="Comprehensive textbook on deep learning.",
            ),
        ]
        db.session.add_all(books)
        db.session.commit()


# Run DB setup once when the app starts (Flask 3+ safe version)
with app.app_context():
    create_tables_and_seed()


@app.route("/")
def home():
    return redirect(url_for("list_books"))


@app.route("/books")
def list_books():
    books = Book.query.order_by(Book.title).all()
    return render_template("index.html", books=books)


@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = (
        Review.query.filter_by(book_id=book.id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return render_template("book_detail.html", book=book, reviews=reviews)


@app.route("/books/<int:book_id>/reviews", methods=["POST"])
def add_review(book_id):
    book = Book.query.get_or_404(book_id)

    username = request.form.get("username", "").strip()
    rating = request.form.get("rating", "").strip()
    comment = request.form.get("comment", "").strip()

    # Basic validation
    if not username or not rating or not comment:
        flash("All fields are required.", "error")
        return redirect(url_for("book_detail", book_id=book.id))

    try:
        rating_value = int(rating)
        if rating_value < 1 or rating_value > 5:
            raise ValueError
    except ValueError:
        flash("Rating must be a number between 1 and 5.", "error")
        return redirect(url_for("book_detail", book_id=book.id))

    review = Review(
        book_id=book.id,
        username=username,
        rating=rating_value,
        comment=comment,
    )
    db.session.add(review)
    db.session.commit()

    flash("Your review has been added!", "success")
    return redirect(url_for("book_detail", book_id=book.id))


if __name__ == "__main__":
    # Local development only
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
