from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from data_models import Author, Book, Base
from sqlalchemy import create_engine, and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/library.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

engine = create_engine('sqlite:///data/library.sqlite')

Session = sessionmaker(bind=engine)
session = Session()


# db.create_all()


@app.route('/', methods=['GET'])
def home_page():
    """A simple homepage that shows all the books in the database"""
    books = session.query(Book).all()
    return render_template('home.html', books=books)


@app.route('/home_search', methods=['GET', 'POST'])
def home_search():
    """This method lets the user search for books by their title or by author"""
    if request.method == 'POST':
        search = request.form.get("search")
        books = []
        title_results = session.query(Book).join(Author).filter(Book.title.like(f'%{search}%')).all()
        author_results = session.query(Book).join(Author).filter(Author.author_name.like(f'%{search}%')).all()
        for title in title_results:
            books.append(title)
        for author in author_results:
            books.append(author)
        if len(books) == 0:
            return "Couldn't find any results similar to your search"
        return render_template('home.html', books=books)
    return render_template('home_search.html')


@app.route('/sort_title', methods=['GET'])
def sort_title():
    """This method sorts the books by their title"""
    books = session.query(Book). \
        order_by(Book.title.desc()). \
        all()
    return render_template('home.html', books=books)


@app.route('/sort_author', methods=['GET'])
def sort_author():
    """This method sorts the books based on the books authors"""
    sorted_books = session.query(Book). \
        join(Author). \
        order_by(Author.author_name, Book.title). \
        all()
    return render_template('home.html', books=sorted_books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Simple method to add an author to the database"""
    if request.method == 'POST':
        author = Author(
            author_id=request.form.get('id'),
            author_name=request.form.get('name'),
            birth_date=request.form.get('birthdate'),
            death_date=request.form.get('date_of_death')
        )

        session.add(author)
        session.commit()

        return f"The author has successfully been added"

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Simple method to add a book to the database"""
    if request.method == 'POST':
        book = Book(
            book_id=request.form.get('id'),
            isbn=request.form.get('isbn'),
            title=request.form.get('title'),
            publication_year=request.form.get('publication_year'),
            author_id=request.form.get('author_id')
        )

        session.add(book)
        session.commit()

        return f"The book has successfully been added"

    return render_template('add_book.html')


@app.route('/book/<int:book_id>/<int:author_id>/delete', methods=['POST'])
def delete_book(book_id, author_id):
    """This method is kind of intricate and confusing but basically it gets the author based on the book
    that is clicked on to be deleted and if the author doesn't have any other books in the database,
    the author is then deleted as well"""

    session.query(Book).filter(Book.book_id == book_id).delete()
    author_books = session.query(Book).filter(Book.author_id == author_id).all()
    if len(author_books) == 0 or len(author_books) is None:
        session.query(Author).filter(Author.author_id == author_id).delete()
        session.commit()
    session.commit()
    books = session.query(Book).all()
    return render_template('book_deleted_home_page.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
