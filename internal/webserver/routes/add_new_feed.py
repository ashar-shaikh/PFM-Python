from flask import Blueprint, jsonify, g, request
from flask import current_app as s
import internal.storage.models as m

endpoint_new_feed = 'add_new_feed'
add_new_feed_bp = Blueprint(endpoint_new_feed, __name__)


@add_new_feed_bp.route('/' + endpoint_new_feed, methods=['POST'])
def new_feed():
    ctx = g.context
    storage = s.storage

    with storage as session:
        try:
            url = request.json.get('url')
            if not url:
                return g.server.handle_error("url is required", 0, 400, ctx)

            language = request.json.get('language', 'en')

            feed = m.RSSFeeds()
            feed.feed_link = url
            # Check if the feed already exists
            existing_feed = storage.execute(m.RSSFeeds.get_feed_by_link, feed_link=url, context=ctx)
            if existing_feed:
                return g.server.handle_error("Feed already exists", 0, 400, ctx)

            # If no existing feed, create a new one
            feed.lang = language
            feed.is_active = True
            is_success, _, err = storage.add(feed, ctx, session=session)
            if is_success:
                # Check if the feed was added successfully
                added_feed = storage.execute(m.RSSFeeds.get_feed_by_link, session=session, feed_link=url, context=ctx)
                if added_feed:
                    return g.server.handle_response(added_feed.get(), ctx)
                else:
                    return g.server.handle_error("Failed to verify the new feed", 0, 500, ctx)
            else:
                return g.server.handle_error(err, 0, 500, ctx)
        except Exception as e:
            return g.server.handle_error(str(e), 0, 500, ctx)
