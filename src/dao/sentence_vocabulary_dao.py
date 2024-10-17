from typing import Tuple, List

from src.db.engine import DbSession
from src.db.entity import Sentence, Vocabulary, SentenceVocabulary
from src.dto.html_dto import SentenceWords


class SentenceVocabularyDao:
    @staticmethod
    def batch_add(source_type: int, source_id: int, sentences: List[SentenceWords]):
        with DbSession() as session:
            for s in sentences:
                for w in s.words:
                    SentenceVocabularyDao.add_or_update(session, source_type, source_id, s.no, s.text, w)
            session.commit()

    @staticmethod
    def add_or_update(session, source_type: int, source_id: int, sentence_no, sentence: str, word: str):
        s = session.query(Sentence).filter(
            Sentence.source_type == source_type,
            Sentence.source_id == source_id,
            Sentence.sentence_no == sentence_no
        ).first()

        if not s:
            s = Sentence(text=sentence, source_type=source_type, source_id=source_id, sentence_no=sentence_no)
            session.add(s)

        w = session.query(Vocabulary).filter(Vocabulary.word == word).first()
        if not w:
            w = Vocabulary(word=word)
            session.add(w)

        r = session.query(SentenceVocabulary).filter(
            SentenceVocabulary.sentence_id == s.id,
            SentenceVocabulary.vocabulary_id == w.id
        ).first()
        if not r:
            r = SentenceVocabulary(sentence_id=s.id, vocabulary_id=w.id)
            session.add(r)


