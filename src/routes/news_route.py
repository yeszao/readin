from flask import Blueprint, render_template, request

from src.db.news_dao import NewsDao

bp = Blueprint('news', __name__)


@bp.get('/news.html')
def get_all_news():
    page = request.args.get('page', 1, int)
    all_news = NewsDao.get_all_news(page, size=10)
    return render_template('news-home.html',
                           all_news=all_news,
                           page=page,
                           news_count=len(all_news)
                           )


@bp.get('/news/<id>.html')
def get_news(id: int):
    news = NewsDao.get_by_id(id)
    if not news:
        return "News not found", 404

    return render_template('news.html', news=news)

