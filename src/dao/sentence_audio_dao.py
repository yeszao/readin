from src.db.engine import DbSession
from src.db.entity import SentenceAudio


class SentenceAudioDao:
    @staticmethod
    def get_one(sentence_id: int, voice: str) -> SentenceAudio:
        with DbSession() as session:
            return session.query(SentenceAudio).filter(
                SentenceAudio.sentence_id == sentence_id,
                SentenceAudio.voice == voice
            ).first()

    @staticmethod
    def add_one(sentence_id: int, voice: str, audio_content: bytes) -> SentenceAudio:
        with DbSession() as session:
            st = SentenceAudio(sentence_id=sentence_id, voice=voice, audio=audio_content)
            session.add(st)
            session.commit()
            return st

