import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.constants.config import BOOKS_DIR, LOG_DIR
from src.dao.book_dao import BookDao
from src.db.entity import Book
from src.utils.html_utils import check_tags
from src.utils.logging_utils import init_logging


def check_unexpected_tags(book: Book):
    futures = []
    with ThreadPoolExecutor() as executor:
        for file in BOOKS_DIR.joinpath(book.slug).glob('*.html'):
            original_content = file.read_text()
            futures.append(executor.submit(check_tags, original_content))

    unexpected_tags = set()
    for future in as_completed(futures):
        unexpected_tags.update(future.result())

    LOG_DIR.joinpath(f"unexpected_tags-{book.slug}.log").write_text('\n'.join(unexpected_tags))
    logging.info(f"[{len(unexpected_tags)}] unexpected tags for book {book.name} written to file.")


if __name__ == '__main__':
    init_logging(LOG_DIR.joinpath("validate-tags.log"))
    for b in BookDao.get_all():
        check_unexpected_tags(b)

    print("All done!")
