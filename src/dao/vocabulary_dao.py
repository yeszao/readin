from authlib.oidc.core import UserInfo

from src.constants.config import TRIAL_PERIOD
from src.db.engine import DbSession
from src.db.entity import User, Vocabulary
from src.utils.date_utils import get_now, get_delta_days


class VocabularyDao:
    @staticmethod
    def add_one(word: str):
        with DbSession() as session:
            session.add(Vocabulary(word=word))
            session.commit()


