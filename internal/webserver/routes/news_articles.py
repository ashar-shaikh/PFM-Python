from flask import Blueprint, jsonify
import internal.resources.rss_feed as rss

news_article_bp = Blueprint('news-articles', __name__)


@news_article_bp.route('/news-articles', methods=['GET'])
def news_article():
    params = {
        rss.STOCK_SYMBOL: ['NESTLE'],
        rss.LANGUAGE: 'en',
        rss.BEFORE_DATE: '2021-12-31',
        rss.AFTER_DATE: '2021-01-01',
        rss.COUNTRY: 'PK'
    }
    rss_feed = rss.new_rss_feed(params)
    articles = rss_feed.fetch_results()
    article_data = []
    if articles:
        for article in articles:
            article_data.append({
                'title': article['title'],
                'link': article['link'],
                'description': article['description'],
                'published': article['published'],
                'source': article['source']
            })
        return jsonify(article_data)
    else:
        return jsonify({"error": "Failed to retrieve market data"}), 500
