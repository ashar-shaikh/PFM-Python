from flask import Flask
import internal.webserver.routes as routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes.market_summary_bp)
    app.register_blueprint(routes.news_article_bp)
    return app
