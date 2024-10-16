import json
from flask import Blueprint, render_template

from src.constants.config import BOOKS_GENERATED_DIR
from src.dao.book_dao import BookDao
from src.dao.chapter_dao import ChapterDao
from src.utils.book_utils import get_prev_next_chapter_urls

bp = Blueprint('book', __name__)


@bp.get('/<book_slug>.html')
def get_book(book_slug: str):
    book = BookDao.get_by_slug(book_slug)
    summary = json.loads(BOOKS_GENERATED_DIR.joinpath(book.slug).joinpath("summary.json").read_text())
    chapters = ChapterDao.get_all(book.id)
    return render_template('book.html',
                           book=book,
                           summary=summary,
                           max_word_count=max(summary['vocabulary_distribution'].values()),
                           chapters=chapters)


@bp.get('/<book_slug>/<chapter_no>.html')
def get_chapter(book_slug: str, chapter_no: str):
    book = BookDao.get_by_slug(book_slug)
    chapter = ChapterDao.get_one(book.id, int(chapter_no))

    prev_chapter_url, next_chapter_url = get_prev_next_chapter_urls(book, int(chapter_no))
    return render_template('chapter.html',
                           book=book,
                           chapter=chapter,
                           prev_chapter_url=prev_chapter_url,
                           next_chapter_url=next_chapter_url,
                           content=chapter.tagged_content_html)
