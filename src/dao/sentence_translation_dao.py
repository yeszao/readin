from src.db.engine import DbSession
from src.db.entity import SentenceTranslation


class SentenceTranslationDao:
    @staticmethod
    def remove_all(sentence_id: int):
        with DbSession() as session:
            session.query(SentenceTranslation).filter(
                SentenceTranslation.sentence_id == sentence_id
            ).delete()
