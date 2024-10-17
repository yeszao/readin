from typing import List

import spacy
from spacy.language import Language

nlp: Language = spacy.load("en_core_web_sm")


def nlp_get_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def nlp_get_words(text: str):
    return nlp(text)
