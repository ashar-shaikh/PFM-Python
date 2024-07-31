from .news_articles import news_article_bp
from .market_summary import market_summary_bp
from .add_new_feed import add_new_feed_bp

handlers = {
    'market_summary': {
        'blueprint': market_summary_bp,
        'secure': True,
    },
    'news_article': {
        'blueprint': news_article_bp,
        'secure': False,
    },
    'add_new_feed': {
        'blueprint': add_new_feed_bp,
        'secure': True,
    },
}
