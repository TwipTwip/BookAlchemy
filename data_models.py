from sqlalchemy import Column, create_engine, Date, Integer, String, update, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///data/library.sqlite')


class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, autoincrement="auto")
    author_name = Column(String)
    birth_date = Column(String)
    death_date = Column(String)

    def __repr__(self) -> str:
        return f"Author(author_id = {self.author_id}, name = {self.author_name})"


class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement="auto")
    isbn = Column(String)
    title = Column(String)
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.author_id"))

    def __repr__(self) -> str:
        return f"Book(book_id = {self.book_id}, title = {self.title})"


Base.metadata.create_all(engine)