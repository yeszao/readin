from src.db.engine import DbSession
from src.db.entity import Sentence, SentenceVocabulary, SentenceTranslation, SentenceAudio
from src.utils.hash_utils import int_hash


class SentenceDao:
    @staticmethod
    def get_one(source_type: int, source_id: int, sentence_no: int) -> Sentence:
        with DbSession() as session:
            return session.query(Sentence).filter(
                Sentence.source_type == source_type,
                Sentence.source_id == source_id,
                Sentence.sentence_no == sentence_no
            ).first()

    @staticmethod
    def remove_all(source_type: int, source_id: int):
        with DbSession() as session:
            sentences = session.query(Sentence).filter(
                Sentence.source_type == source_type,
                Sentence.source_id == source_id
            ).all()

            ids = [s.id for s in sentences]
            session.query(SentenceVocabulary).filter(SentenceVocabulary.sentence_id.in_(ids)).delete()
            session.query(SentenceAudio).filter(SentenceAudio.sentence_id.in_(ids)).delete()
            session.query(SentenceTranslation).filter(SentenceTranslation.sentence_id.in_(ids)).delete()
            session.query(Sentence).filter(Sentence.id.in_(ids)).delete()
            session.commit()
