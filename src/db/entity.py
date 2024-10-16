from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, UniqueConstraint, LargeBinary, ForeignKey
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from src.db.engine import Base, DbEngine


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    name = Column(String(50), nullable=False, default='')
    slug = Column(String(50), nullable=False, unique=True)
    author = Column(String(100), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    cover = Column(String(200), nullable=False, default='')
    description = Column(String(300), nullable=False, default='')

    sentence_count = Column(Integer, nullable=False, default=0)
    word_count = Column(Integer, nullable=False, default=0)
    vocabulary_count = Column(Integer, nullable=False, default=0)


class PostBase(Base):
    __abstract__ = True

    tagged_content_html = Column(MEDIUMTEXT, nullable=False, default='')
    sentence_count = Column(Integer, nullable=False, default=0)
    word_count = Column(Integer, nullable=False, default=0)
    vocabulary_count = Column(Integer, nullable=False, default=0)


class News(PostBase):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    title = Column(String(250), nullable=False, default='')
    tagged_title = Column(String(300), nullable=False, default='')
    content_html = Column(Text, nullable=False, default='')
    url = Column(String(300), nullable=False, unique=True, default='')
    publication = Column(String(10), nullable=False)
    date = Column(DateTime, nullable=False, index=True)


class Chapter(PostBase):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    book_id = Column(Integer, nullable=False)
    no = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('book_id', 'no'),
    )


class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    source_type = Column(Integer, nullable=False)    # 1: News, 2: Chapter
    source_id = Column(Integer, nullable=False)
    sentence_no = Column(Integer, nullable=False)
    text = Column(String(2000), nullable=False)

    __table_args__ = (
        UniqueConstraint('source_id', "sentence_no",  'source_type'),
    )


class SentenceAudio(Base):
    __tablename__ = 'sentence_audios'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    sentence_id = Column(Integer, ForeignKey('sentences.id'))
    voice = Column(String(10), nullable=False)
    audio = Column(LargeBinary, nullable=False)


class SentenceTranslation(Base):
    __tablename__ = 'sentence_translations'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    sentence_id = Column(Integer, ForeignKey('sentences.id'))
    lang = Column(String(10), nullable=False)
    translation = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint('sentence_id', 'lang'),
    )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    oauth_id = Column(String(50), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    name = Column(String(80), nullable=False, default="")
    premium_expired_at = Column(DateTime, nullable=False)
    last_login_at = Column(DateTime, nullable=False, default=datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Vocabulary(Base):
    __tablename__ = 'vocabulary'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    word = Column(String(50), nullable=False, unique=True)


class Glossary(Base):
    __tablename__ = 'glossaries'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('users.id'))
    vocabulary_id = Column(Integer, ForeignKey('vocabulary.id'))

    __table_args__ = (
        UniqueConstraint('user_id', 'vocabulary_id'),
    )


class SentenceVocabulary(Base):
    __tablename__ = 'sentence_vocabulary'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    sentence_id = Column(Integer, ForeignKey('sentences.id'))
    vocabulary_id = Column(Integer, ForeignKey('vocabulary.id'))

    __table_args__ = (
        UniqueConstraint('sentence_id', 'vocabulary_id'),
    )


if __name__ == '__main__':
    Base.metadata.create_all(DbEngine)
