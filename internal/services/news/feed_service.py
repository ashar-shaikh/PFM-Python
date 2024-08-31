from internal.storage.models import RSSFeeds


class FeedService:
    def __init__(self, storage, context, session):
        self.storage = storage
        self.context = context
        self.session = session

    def add_feed(self, url, language='en'):
        # Check if the feed already exists
        existing_feed = self.storage.execute(RSSFeeds.get_feed_by_link, feed_link=url, context=self.context)
        if existing_feed:
            return None, "Feed already exists"

        # Create a new feed
        feed = RSSFeeds()
        feed.feed_link = url
        feed.lang = language
        feed.is_active = True
        is_success, _, err = self.storage.add(feed, self.context, session=self.session)

        if not is_success:
            return None, err

        # Verify the new feed was added
        added_feed = self.storage.execute(RSSFeeds.get_feed_by_link, session=self.session, feed_link=url,
                                          context=self.context)
        if not added_feed:
            return None, "Failed to verify the new feed"

        return added_feed.get(), None
