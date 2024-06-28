from flask import Flask
from .routes.market_summary import market_summary_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(market_summary_bp)
    return app
