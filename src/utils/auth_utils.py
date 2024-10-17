from functools import wraps
from flask import session

from src.dao.user_dao import UserDao
from src.utils.date_utils import is_future
from src.dto.json_dto import Json


def is_logged_in() -> bool:
    return "user" in session and session["user"] is not None


def is_logged_out() -> bool:
    return not is_logged_in()


def api_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_logged_out():
            return Json.error("Please login to use.", 401)

        return func(*args, **kwargs)
    return wrapper


def api_payment_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_logged_out():
            return Json.error("Please login."), 401

        if not is_premium():
            return Json.error(f"Please upgrade to premium."), 403

        return func(*args, **kwargs)
    return wrapper


def is_premium() -> bool:
    if is_logged_out():
        return False

    if is_future(session["user"]["premium_expired_at"]):
        return True

    user = UserDao.get_user_by_id(session["user"]["id"])
    return is_future(user.premium_expired_at)
