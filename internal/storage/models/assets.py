from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, Boolean, DateTime
from internal.storage.models.base import Base


class Assets(Base):
    """
    Assets model represents the assets.

    Fields:
    - id: Integer, Primary Key, auto-incrementing.
    - ticker_symbol: String(10), Not Null, Unique. Represents the ticker symbol of the asset.
    - asset_name: String(255), Not Null. Represents the name of the asset.
    - asset_type: String(50), Not Null, Default: 'stock'. Represents the type of the asset.
    - description: String(250). Represents the description of the asset.
    - market: String(50), Not Null, Default: 'PSX'. Represents the market of the asset.
    - sector: String(100). Represents the sector of the asset.
    - industry: String(100). Represents the industry of the asset.
    - country: String(100), Default: 'PK'. Represents the country of the asset.
    - currency: String(3), Not Null, Default: 'PKR'. Represents the currency of the asset.
    - created_at: DateTime, Default: datetime.utcnow. Timestamp when the record was created.
    - updated_at: DateTime, Default: datetime.utcnow, onupdate: datetime.utcnow. Timestamp when the record was last updated.
    """

    __tablename__ = 'assets'
    id = Column(Integer, Sequence('assets_id_seq'), primary_key=True)
    ticker_symbol = Column(String(10), nullable=False, unique=True)
    asset_name = Column(String(255), nullable=False)
    asset_type = Column(String(50), nullable=False, default='stock')
    description = Column(String(250))
    market = Column(String(50), nullable=False, default='PSX')
    sector = Column(String(100))
    industry = Column(String(100))
    country = Column(String(100), default='PK')
    currency = Column(String(3), nullable=False, default='PKR')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get(self):
        data = {
            'id': self.id,
            'ticker_symbol': self.ticker_symbol,
            'asset_name': self.asset_name,
            'asset_type': self.asset_type,
            'description': self.description,
            'market': self.market,
            'sector': self.sector,
            'industry': self.industry,
            'country': self.country,
            'currency': self.currency,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data
