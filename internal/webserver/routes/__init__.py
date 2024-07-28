from .news_articles import news_article_bp
from .market_summary import market_summary_bp

handlers = {
        'market_summary': {
            'blueprint': market_summary_bp,
            'secure': True,
        },
        'news_article': {
            'blueprint': news_article_bp,
            'secure': False,
        },
    }