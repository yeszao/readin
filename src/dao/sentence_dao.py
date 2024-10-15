from src.db.engine import DbSession
from src.db.entity import Sentence
from src.utils.hash_utils import int_hash


class SentenceDao:
    @staticmethod
    def get_one(sentence: str, lang: str) -> Sentence:
        sentence = sentence.strip()
        with DbSession() as session:
            return session.query(Sentence)\
                .filter(
                Sentence.sentence_hash == int_hash(sentence),
                Sentence.sentence == sentence,
                Sentence.lang == lang
            ).first()

    @staticmethod
    def add_one(sentence: str, lang: str, translation: str):
        sentence = sentence.strip()
        with DbSession() as session:
            session.add(Sentence(
                sentence_hash=int_hash(sentence),
                sentence=sentence,
                lang=lang,
                translation=translation
            ))
            session.commit()
