from typing import List, Set
from pydantic import BaseModel


class SentenceWords(BaseModel):
    no: int
    text: str
    words: Set[str]


class ParsedHtml(BaseModel):
    tagged_content_html: str = ''

    sentence_count: int = 0
    word_count: int = 0
    vocabulary_count: int = 0

    sentences: List[SentenceWords] = []
    vocabulary: Set[str] = set()




