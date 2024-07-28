from flask import Blueprint, jsonify, request
import internal.resources.rss_feed as rss

news_endpoint = 'news_articles'
news_article_bp = Blueprint(news_endpoint, __name__)


@news_article_bp.route('/' + news_endpoint, methods=['GET'])
def news_article():
    rss_feed = rss.new_rss_feed()
    articles, count = rss_feed.fetch_results()
    article_data = []
    if articles:
        for article in articles:
            article_data.append({
                'id': article['id'] if 'id' in article else None,
                'title': article['title'] if 'title' in article else 'Unknown',
                'link': article['link'] if 'link' in article else 'Unknown',
                'description': article['description'] if 'description' in article else 'Unknown',
                'published': article['published'].strftime('%Y-%m-%d %H:%M:%S') if 'published' in article else 'Unknown',
                'source': article['source'] if 'source' in article else 'Unknown'
            })

        return jsonify({"status": "success","data": article_data,"count": count}), 200
    else:
        return jsonify({"status": "error","data": {},"message": "No Records Found"}), 404
