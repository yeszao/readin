from src.db.engine import DbSession
from src.db.entity import Chapter


class ChapterDao:
    @staticmethod
    def merge(chapter: Chapter) -> int:
        with DbSession() as session:
            r = session.query(Chapter).filter(
                Chapter.book_id == chapter.book_id,
                Chapter.no == chapter.no
            ).first()
            if r:
                session.query(Chapter).filter(Chapter.id == r.id).update({
                    'tagged_content_html': chapter.tagged_content_html,
                    'sentence_count': chapter.sentence_count,
                    'word_count': chapter.word_count,
                    'vocabulary_count': chapter.vocabulary_count
                })
                session.commit()
                return r.id

            session.add(chapter)
            session.commit()
            return chapter.id

    @staticmethod
    def add_one(chapter: Chapter) -> int:
        with DbSession() as session:
            session.add(chapter)
            session.commit()
            return chapter.id

    @staticmethod
    def get_one(book_id: int, chapter_no: int) -> Chapter:
        with DbSession() as session:
            return session.query(Chapter).filter(
                Chapter.book_id == book_id,
                Chapter.no == chapter_no
            ).first()

    @staticmethod
    def get_all(book_id: int):
        with DbSession() as session:
            return session.query(Chapter).filter(
                Chapter.book_id == book_id
            ).order_by(Chapter.no.asc()).all()