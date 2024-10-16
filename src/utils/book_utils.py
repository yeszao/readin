import json
from flask import url_for

from src.constants.config import BOOKS_DIR
from src.db.entity import Book


def get_prev_next_chapter_urls(book: Book, chapter_no: int) -> (str, str):
    prev_chapter = chapter_no - 1
    next_chapter = chapter_no + 1
    prev_chapter_url = generate_chapter_url(book.slug, prev_chapter) if prev_chapter >= 1 else None
    next_chapter_url = generate_chapter_url(book.slug, next_chapter) if next_chapter <= book.chapter_number else None
    return prev_chapter_url, next_chapter_url


def generate_chapter_url(book_slug: str, chapter_no: int) -> str:
    return url_for('book.get_chapter', book_slug=book_slug, chapter_no=chapter_no)


def get_book_dicts():
    return json.loads(BOOKS_DIR.joinpath("books.json").read_text())

