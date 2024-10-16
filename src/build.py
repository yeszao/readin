import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.constants.config import BOOKS_DIR, LOG_DIR
from src.constants.enums import SentenceSource
from src.dao.book_dao import BookDao
from src.dao.chapter_dao import ChapterDao
from src.dao.sentence_vocabulary_dao import SentenceVocabularyDao
from src.db.entity import Book, Chapter
from src.utils.chapter_utils import tagged_html
from src.utils.logging_utils import init_logging


def parse_chapter(chapter_no: int, original_content: str):
    tagged_content, sentences, chapter_vocabulary, chapter_word_count = tagged_html(original_content)
    print(f"chapter #{chapter_no} parsed.")

    return chapter_no, tagged_content, sentences, chapter_vocabulary, chapter_word_count


def build_book(book: Book):
    logging.info(f"[[{book.name}]] started.")

    book_vocabulary = set()
    book_word_count = 0
    book_sentence_total = 0
    futures = []
    with ThreadPoolExecutor() as executor:
        for file in BOOKS_DIR.joinpath(book.slug).glob('*.html'):
            chapter_no = int(file.stem)
            original_content = file.read_text()
            futures.append(executor.submit(parse_chapter, chapter_no, original_content))

    for future in as_completed(futures):
        chapter_no, tagged_content, sentences, chapter_vocabulary, chapter_word_count = future.result()

        chapter = Chapter()
        chapter.no = chapter_no
        chapter.book_id = book.id

        chapter.tagged_content_html = tagged_content
        chapter.sentence_count = len(sentences)
        chapter.word_count = chapter_word_count
        chapter.vocabulary_count = len(chapter_vocabulary)
        chapter_id = ChapterDao.merge(chapter)

        # todo: don't update sentences if the count of sentence in a chapter is the same
        SentenceVocabularyDao.batch_add(SentenceSource.CHAPTER.value, chapter_id, sentences)

        book_sentence_total += len(sentences)
        book_vocabulary.update(chapter_vocabulary)
        book_word_count += chapter_word_count
        logging.info(f"chapter #{chapter_no} saved.")

    BookDao.update_counts(book.id, book_sentence_total, book_word_count, len(book_vocabulary))
    logging.info(f"[[{book.name}]] generated.")


if __name__ == '__main__':
    init_logging(LOG_DIR.joinpath("build.log"))
    for b in BookDao.get_all():
        build_book(b)

    logging.info("All done!")
