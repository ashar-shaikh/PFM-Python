from flask import Blueprint, jsonify, g, request
from flask import current_app as s
import internal.storage.models as m

endpoint_new_feed = 'add_new_feed'
add_new_feed_bp = Blueprint(endpoint_new_feed, __name__)


@add_new_feed_bp.route('/' + endpoint_new_feed, methods=['POST'])
def new_feed():
    ctx = g.context
    url = request.json.get('url')
    if not url:
        return g.server.handle_error("url is required", 1, 400, ctx)
    language = request.json.get('language')
    if not language:
        language = 'en'

    data = m.RSSFeeds()
    rss_data, err = s.storage.get(data, None, ctx, feed_link=url)
    if rss_data:
        return g.server.handle_error("feed already exists", 1, 400, ctx)
    if err:
        return g.server.handle_error(err, 2, 500, ctx)

    data.feed_link = url
    data.lang = language
    data.is_active = 1
    is_success, err = s.storage.add(data, ctx)
    if is_success:
        return g.server.handle_response(data.get(), ctx)
    else:
        return g.server.handle_error(err, 2, 500, ctx)
