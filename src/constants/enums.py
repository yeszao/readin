from enum import Enum


class Publication(Enum):
    BBC = 'BBC'
    CNN = 'CNN'


class SentenceSource(Enum):
    CHAPTER = 1
    NEWS = 2
