from authlib.oidc.core import UserInfo

from src.config import TRIAL_PERIOD
from src.db.engine import DbSession
from src.db.entity import User
from src.utils.date_utils import get_now, get_delta_days


class UserDao:
    @staticmethod
    def get_or_add_user(userinfo: UserInfo) -> dict:
        with DbSession() as session:
            user = session.query(User).filter(User.oauth_id == userinfo["sub"]).first()
            if user:
                user.last_login_at = get_now()
                session.commit()
                return user.as_dict()

            user = session.query(User).filter(User.email == userinfo["email"]).first()
            if user:
                user.last_login_at = get_now()
                session.commit()
                return user.as_dict()

            user = User(
                oauth_id=userinfo["sub"],
                email=userinfo["email"],
                name=userinfo["given_name"],
                last_login_at=get_now(),
                premium_expired_at=get_delta_days(TRIAL_PERIOD),
            )
            session.add(user)
            session.commit()

            return user.as_dict()