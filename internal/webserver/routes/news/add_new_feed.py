from flask import Blueprint, g, request
from flask import current_app as s
from internal.services.news.feed_service import FeedService

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

            # Create an instance of FeedService with the current session, context, and storage
            feed_service = FeedService(storage=storage, context=ctx, session=session)
            result, error = feed_service.add_feed(url, language)

            if error:
                return g.server.handle_error(error, 0, 400, ctx)

            return g.server.handle_response(result, ctx)

        except Exception as e:
            return g.server.handle_error(str(e), 0, 500, ctx)
