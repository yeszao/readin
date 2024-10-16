from typing import List

from src.db.engine import DbSession
from src.db.entity import News, Book


class BookDao:
    @staticmethod
    def get_all():
        with DbSession() as session:
            return session.query(Book).all()

    @staticmethod
    def get_by_slug(slug: str):
        with DbSession() as session:
            return session.query(Book).filter(Book.slug == slug).first()

    @staticmethod
    def update_counts(book_id: int, sentence_count: int, word_count: int, vocabulary_count: int):
        with DbSession() as session:
            session.query(Book).filter(Book.id == book_id).update({
                'sentence_count': sentence_count,
                'word_count': word_count,
                'vocabulary_count': vocabulary_count
            })
            session.commit()
