from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, Boolean, DateTime
from internal.storage.models.base import Base


class RSSFeeds(Base):
    """
    ContentAnalysis model represents the analysis of content.

    Fields:
    - id: Integer, Primary Key, auto-incrementing.
    - content_id: Integer, Not Null, Default: 0. Represents the ID of the content.
    - classification: String(255), Default: "". Classification of the content.
    - sentiment: String(50), Default: "". Sentiment of the content.
    - summary: String(400), Default: "". Summary of the content.
    - created_at: DateTime, Default: datetime.utcnow. Timestamp when the record was created.
    - updated_at: DateTime, Default: datetime.utcnow, onupdate: datetime.utcnow. Timestamp when the record was last updated.
    """

    __tablename__ = 'rss_feeds'
    id = Column(Integer, Sequence('rss_feeds_id_seq'), primary_key=True)
    feed_link = Column(String, nullable=False)
    lang = Column(String(2), nullable=True, default='en')
    is_active = Column(Boolean, nullable=False, default=True)
    last_successfully_monitored = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_feed_by_link(cls, session, feed_link):
        try:
            return session.query(cls).filter_by(feed_link=feed_link).first()
        except Exception as e:
            raise e
