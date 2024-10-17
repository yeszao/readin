import json
import logging

from src.constants.config import CACHE_DIR, LOG_DIR
from src.constants.enums import SentenceSource
from src.dao.sentence_vocabulary_dao import SentenceVocabularyDao
from src.db.entity import News
from src.utils.html_utils import tagged_html, wrap_title
from src.utils.date_utils import get_now_filename, str_to_datetime
from src.utils.google_news_utils import parse_cnn, parse_bbc, get_google_news, check_url, get_html
from src.dao.news_dao import NewsDao
from src.utils.logging_utils import init_logging

publications = {
    "CNN": {
        "name": "CNN",
        "html_parser": parse_cnn,
    },
    "BBC.com": {
        "name": "BBC",
        "html_parser": parse_bbc,
    }
}

if __name__ == '__main__':
    init_logging(LOG_DIR.joinpath("crawl_news.log"))
    news_results = get_google_news()
    CACHE_DIR.joinpath("news").mkdir(parents=True, exist_ok=True)
    CACHE_DIR.joinpath("news").joinpath(f"{get_now_filename()}.json").write_text(json.dumps(news_results, indent=2))

    for result in news_results['news_results']:
        if 'highlight' not in result:
            continue

        source_name = result['highlight']['source']['name']
        if source_name not in publications:
            continue

        url = check_url(result)
        if not url:
            continue

        if NewsDao.get_by_url(url):
            continue

        html = get_html(url)
        content_html = publications[source_name]['html_parser'](html)
        if not content_html:
            logging.error(f"Failed to get html content from {url}")
            continue

        parsed = tagged_html(content_html)

        title = result['highlight']['title']
        parsed_title = tagged_html("<h1>" + title + "</h1>")

        news = News(
            url=url,
            publication=publications[source_name]['name'],
            title=title,
            tagged_title=wrap_title(title),
            content_html=content_html,
            tagged_content_html=parsed.tagged_content_html,
            sentence_count=parsed.sentence_count,
            vocabulary_count=parsed.vocabulary_count,
            word_count=parsed.word_count,
            date=str_to_datetime(result['highlight']['date'])
        )

        news_id = NewsDao.add_one(news)
        SentenceVocabularyDao.batch_add(SentenceSource.NEWS.value, news_id, parsed.sentences)
        logging.info(f"Saved [{publications[source_name]['name']}] {url}")
