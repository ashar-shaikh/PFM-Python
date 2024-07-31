from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from internal.storage.models.base import Base


class ContentAnalysis(Base):
    """
    Content Analysis Model

    Fields:
    id (int): Primary Key
    content_id (int): Content ID
    classification (str): Classification of the content
    sentiment (str): Sentiment of the content
    summary (str): Summary of the content
    created_at (datetime): Created at timestamp
    updated_at (datetime): Updated at timestamp
    """
    __tablename__ = 'content_analysis'
    id = Column(Integer, Sequence('content_analysis_id_seq'), primary_key=True)
    content_id = Column(Integer, nullable=False)
    classification = Column(String(255))
    sentiment = Column(String(50))
    summary = Column(String(400))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get(self):
        data = {
            'id': self.id,
            'content_id': self.content_id,
            'classification': self.classification,
            'sentiment': self.sentiment,
            'summary': self.summary,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data
