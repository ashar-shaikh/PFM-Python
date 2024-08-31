from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from internal.storage.models.generic.base import Base


class DailyTradedAssetPosition(Base):
    """
    Daily Traded Asset Position Model

    Fields:
    - id: Integer, Primary Key, auto-incrementing.
    - asset_id: Integer, Not Null. Represents the ID of the asset.
    - open_price: Decimal(9, 2), Not Null. Represents the opening price of the asset.
    - close_price: Decimal(9, 2), Not Null. Represents the closing price of the asset.
    - high_price: Decimal(9, 2), Not Null. Represents the high price of the asset.
    - low_price: Decimal(9, 2), Not Null. Represents the low price of the asset.
    - volume_traded: Decimal(16, 2), Not Null. Represents the volume traded of the asset.
    - timestamp: DateTime, Default: datetime.utcnow. Represents the timestamp of the record.
    - created_at: DateTime, Default: datetime.utcnow. Timestamp when the record was created.
    - updated_at: DateTime, Default: datetime.utcnow, onupdate: datetime.utcnow. Timestamp when the record was last updated.
    """

    __tablename__ = 'daily_traded_asset_position'
    id = Column(Integer, Sequence('daily_traded_asset_position_id_seq'), primary_key=True)
    asset_id = Column(Integer, nullable=False)
    open_price = Column(String(255), nullable=False)
    close_price = Column(String(255), nullable=False)
    high_price = Column(String(255), nullable=False)
    low_price = Column(String(255), nullable=False)
    volume_traded = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get(self):
        data = {
            'id': self.id,
            'asset_id': self.asset_id,
            'open_price': self.open_price,
            'close_price': self.close_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'volume_traded': self.volume_traded,
            'timestamp': self.timestamp,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data