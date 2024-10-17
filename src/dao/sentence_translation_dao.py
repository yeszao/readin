from src.db.engine import DbSession
from src.db.entity import SentenceTranslation


class SentenceTranslationDao:
    @staticmethod
    def get_one(sentence_id: int, lang: str) -> SentenceTranslation:
        with DbSession() as session:
            return session.query(SentenceTranslation).filter(
                SentenceTranslation.sentence_id == sentence_id,
                SentenceTranslation.lang == lang
            ).first()

    @staticmethod
    def add_one(sentence_id: int, lang: str, translation: str) -> SentenceTranslation:
        with DbSession() as session:
            st = SentenceTranslation(sentence_id=sentence_id, lang=lang, translation=translation)
            session.add(st)
            session.commit()
            return st
