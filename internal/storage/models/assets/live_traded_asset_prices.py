from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from internal.storage.models.generic.base import Base


class LiveTradedAssetPrices(Base):
    """
    Live Traded Asset Prices Model

    Fields:
    - id: Integer, Primary Key, auto-incrementing.
    - asset_id: Integer, Not Null. Represents the ID of the asset.
    - price: Decimal(9, 2), Not Null. Represents the price of the asset.
    - volume_traded: Decimal(16, 2), Not Null. Represents the volume traded of the asset.
    - timestamp: DateTime, Default: datetime.utcnow. Represents the timestamp of the record.
    - created_at: DateTime, Default: datetime.utcnow. Timestamp when the record was created.
    - updated_at: DateTime, Default: datetime.utcnow, onupdate: datetime.utcnow. Timestamp when the record was last updated.
    """

    __tablename__ = 'live_traded_asset_prices'
    id = Column(Integer, Sequence('live_traded_asset_prices_id_seq'), primary_key=True)
    asset_id = Column(Integer, nullable=False)
    price = Column(String(255), nullable=False)
    volume_traded = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get(self):
        data = {
            'id': self.id,
            'asset_id': self.asset_id,
            'price': self.price,
            'volume_traded': self.volume_traded,
            'timestamp': self.timestamp,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data
