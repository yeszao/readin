from flask import Flask, request

from src.config import STATIC_VERSION, LOG_DIR
from src.languages import SUPPORTED_LANGUAGES
from src.routes import home_route, auth_route, book_route, news_route, tool_route
from src.utils.date_utils import time_ago
from src.utils.logging_utils import init_logging
from src.utils.number_utils import short_number

app = Flask(__name__)
app.secret_key = 'JDYUF82opufd89sa!@8(u23o'
init_logging(LOG_DIR.joinpath("web.log"))

app.register_blueprint(home_route.bp)
app.register_blueprint(auth_route.bp)
app.register_blueprint(book_route.bp)
app.register_blueprint(news_route.bp)
app.register_blueprint(tool_route.bp)

app.jinja_env.filters['short_number'] = short_number
app.jinja_env.filters['time_ago'] = time_ago

@app.context_processor
def inject_global_variables():
    return dict(
        static_version=STATIC_VERSION,
        languages=SUPPORTED_LANGUAGES,
        user_settings={
            "fontSize": request.cookies.get('fontSize', '16px'),
            "darkMode": request.cookies.get('darkMode', 'light'),
            "language": request.cookies.get('language'),
        },
        sitename="Readmain",
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
