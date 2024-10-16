import json
from flask import Blueprint, render_template

from src.constants.config import HOME_NEWS_NUM, BOOKS_GENERATED_DIR
from src.dao.book_dao import BookDao
from src.dao.news_dao import NewsDao

bp = Blueprint('home', __name__)


@bp.get("/health")
def health():
    return {"alive": True}


@bp.get('/')
def home():
    news = NewsDao.get_latest(HOME_NEWS_NUM)

    summary_file = BOOKS_GENERATED_DIR.joinpath("summary.json")
    summary = json.loads(summary_file.read_text())
    return render_template('home.html', books=BookDao.get_all(), summary=summary, news=news)

