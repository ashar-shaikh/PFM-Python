from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, Boolean, DateTime
from internal.storage.models.base import Base


class RSSFeeds(Base):
    __tablename__ = 'rss_feeds'
    id = Column(Integer, Sequence('rss_feeds_id_seq'), primary_key=True)
    feed_link = Column(String, nullable=False)
    lang = Column(String(2), nullable=True, default='en')
    is_active = Column(Boolean, nullable=False, default=True)
    last_successfully_monitored = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get(self):
        data = {
            'id': self.id,
            'feed_link': self.feed_link,
            'lang': self.lang,
            'is_active': self.is_active,
            'last_successfully_monitored': self.last_successfully_monitored,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data