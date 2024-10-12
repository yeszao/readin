import json

from flask import Blueprint, render_template

from src.config import BOOKS_GENERATED_DIR
from src.utils.book_utils import get_book_slug_map, get_chapters, Chapter, get_prev_next_chapter_urls

bp = Blueprint('book', __name__)


@bp.get('/<book_slug>.html')
def get_book(book_slug: str):
    book = get_book_slug_map()[book_slug]
    summary = json.loads(BOOKS_GENERATED_DIR.joinpath(book.slug).joinpath("summary.json").read_text())
    return render_template('book.html',
                           book=book,
                           summary=summary,
                           max_word_count=max(summary['vocabulary_distribution'].values()),
                           chapters=get_chapters(book))


@bp.get('/<book_slug>/<chapter_no>.html')
def get_chapter(book_slug: str, chapter_no: str):
    book = get_book_slug_map()[book_slug]
    chapter = Chapter(int(chapter_no))
    tagged_html_file = BOOKS_GENERATED_DIR.joinpath(book.slug).joinpath(chapter.html_file)

    prev_chapter_url, next_chapter_url = get_prev_next_chapter_urls(book, int(chapter_no))
    return render_template('chapter.html',
                           book=book,
                           chapter=chapter,
                           prev_chapter_url=prev_chapter_url,
                           next_chapter_url=next_chapter_url,
                           content=tagged_html_file.read_text())
