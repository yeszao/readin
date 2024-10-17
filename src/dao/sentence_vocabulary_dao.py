from typing import List

from src.db.engine import DbSession
from src.db.entity import Sentence, Vocabulary, SentenceVocabulary
from src.dto.html_dto import SentenceWords


class SentenceVocabularyDao:
    @staticmethod
    def _get_or_create_vocab_map(session, sentences):
        unique_words = {w for s in sentences for w in s.words}

        existing_vocab = session.query(Vocabulary).filter(Vocabulary.word.in_(unique_words)).all()
        vocab_map = {v.word: v for v in existing_vocab}

        new_vocab = []
        for word in unique_words:
            if word not in vocab_map:
                voca = Vocabulary(word=word)
                vocab_map[word] = voca
                new_vocab.append(voca)

        if new_vocab:
            session.add_all(new_vocab)
            session.flush()  # Ensure new vocabularies get their IDs

        return vocab_map

    @staticmethod
    def _create_sentences(session, source_type, source_id, sentences):
        sentence_entries = []
        for s in sentences:
            sentence = Sentence(
                text=s.text,
                source_type=source_type,
                source_id=source_id,
                sentence_no=s.no
            )
            sentence_entries.append(sentence)

        # Add all sentences and flush to ensure IDs are generated
        session.add_all(sentence_entries)
        session.flush()
        return sentence_entries

    @staticmethod
    def _create_sentence_vocab_associations(session, sentence_entries, sentences, vocab_map):
        sentence_vocab_entries = []
        for sentence, s in zip(sentence_entries, sentences):
            for w in s.words:
                vocab = vocab_map[w]
                sentence_vocab_entries.append(SentenceVocabulary(
                    sentence_id=sentence.id,
                    vocabulary_id=vocab.id
                ))
        session.add_all(sentence_vocab_entries)

    @staticmethod
    def batch_add(source_type: int, source_id: int, sentences: List[SentenceWords]):
        with DbSession() as session:
            with session.no_autoflush:
                vocab_map = SentenceVocabularyDao._get_or_create_vocab_map(session, sentences)
                sentence_entries = SentenceVocabularyDao._create_sentences(session, source_type, source_id, sentences)
                SentenceVocabularyDao._create_sentence_vocab_associations(session, sentence_entries, sentences, vocab_map)
            session.commit()

    @staticmethod
    def remove_all(sentence_id: int):
        with DbSession() as session:
            session.query(SentenceVocabulary).filter(
                SentenceVocabulary.sentence_id == sentence_id
            ).delete()

