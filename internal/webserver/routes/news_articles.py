from flask import Blueprint, jsonify, request
import internal.resources.rss_feed as rss
news_article_bp = Blueprint('news-articles', __name__)


@news_article_bp.route('/news-articles', methods=['GET'])
def news_article():
    parameter_data = request.args
    stock_symbols = parameter_data.getlist('stock_symbols')
    after_date = parameter_data.get('after_date')
    before_date = parameter_data.get('before_date')

    if not stock_symbols:
        return jsonify({"status": "error","data": {},"message": "stock_symbols are required"}), 400
    if not after_date:
        return jsonify({"status": "error","data": {},"message": "after_date is required"}), 400
    if not before_date:
        return jsonify({"status": "error","data": {},"message": "before_date is required"}), 400

    params = {
        rss.STOCK_SYMBOL: stock_symbols,
        rss.LANGUAGE: 'en',
        rss.AFTER_DATE: after_date,
        rss.BEFORE_DATE:  before_date,
        rss.COUNTRY: 'PK',
        rss.SEARCH_QUERY: 'PSX'
    }
    rss_feed = rss.new_rss_feed(params)
    articles, count = rss_feed.fetch_results()
    article_data = []
    if articles:
        for article in articles:
            article_data.append({
                'id': article['id'],
                'title': article['title'],
                'link': article['link'],
                'description': article['description'],
                'published': article['published'].strftime('%Y-%m-%d %H:%M:%S'),
                'source': article['source']
            })

        return jsonify({"status": "success","data": article_data,"count": count}), 200
    else:
        return jsonify({"status": "error","data": {},"message": "No Records Found"}), 404
