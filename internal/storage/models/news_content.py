import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Boolean
from internal.storage.models.base import Base


class NewsContent(Base):
    __tablename__ = 'news_content'
    id = Column(Integer, Sequence('news_content_id_seq'), primary_key=True)
    feed_id = Column(Integer, nullable=False)
    guid = Column(String(255), nullable=False)
    title = Column(String(255))
    link = Column(String(255))
    pub_date = Column(DateTime)
    description = Column(String)
    content = Column(String)
    is_discarded = Column(Boolean, default=False)
    is_analyzed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get(self):
        data = {
            'id': self.id,
            'feed_id': self.feed_id,
            'guid': self.guid,
            'title': self.title,
            'link': self.link,
            'pub_date': self.pub_date,
            'description': self.description,
            'content': self.content,
            'is_discarded': self.is_discarded,
            'is_analyzed': self.is_analyzed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data