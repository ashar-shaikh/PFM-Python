from flask import Flask
import internal.webserver.routes as routes
import internal.resources.helper.logger as logger


def create_app():
    app: Flask = Flask(__name__)
    # noinspection PyPropertyAccess
    app.logger = logger.LoggerManager(__name__).logger
    app.register_blueprint(routes.market_summary_bp)
    app.register_blueprint(routes.news_article_bp)
    return app
