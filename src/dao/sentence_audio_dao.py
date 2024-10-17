from src.db.engine import DbSession
from src.db.entity import SentenceVocabulary, SentenceAudio


class SentenceAudioDao:

    @staticmethod
    def remove_all(sentence_id: int):
        with DbSession() as session:
            session.query(SentenceAudio).filter(
                SentenceVocabulary.sentence_id == sentence_id
            ).delete()
            session.commit()
