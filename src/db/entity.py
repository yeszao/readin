from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text, UniqueConstraint

from src.db.engine import Base, DbEngine


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    url = Column(String(300), nullable=False, unique=True, default='')
    publication = Column(String(10), nullable=False)
    title = Column(String(250), nullable=False, default='')
    tagged_title = Column(String(300), nullable=False, default='')
    content_html = Column(Text, nullable=False, default='')
    tagged_content_html = Column(Text, nullable=False, default='')
    word_count = Column(Integer, nullable=False, default=0)
    vocabulary_count = Column(Integer, nullable=False, default=0)
    vocabulary = Column(Text, nullable=False, default='')
    date = Column(DateTime, nullable=False, index=True)


class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    sentence_hash = Column(BigInteger, nullable=False)
    sentence = Column(String(500), nullable=False)
    lang = Column(String(10), nullable=False)
    translation = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint('sentence_hash', 'lang', 'sentence'),
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

    def __dict__(self):
        return {
            "id": self.id,
            "oauth_id": self.oauth_id,
            "email": self.email,
            "name": self.name,
            "premium_expired_at": self.premium_expired_at,
            "last_login_at": self.last_login_at
        }


if __name__ == '__main__':
    Base.metadata.create_all(DbEngine)
