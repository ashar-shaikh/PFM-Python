from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from internal.storage.models.generic.base import Base


class Stocks(Base):
    """
    Stocks model represents the stocks.

    Fields:
    - id: Integer, Primary Key, auto-incrementing.
    - asset_id: Integer, Not Null. Foreign Key to Assets table.
    - ticker_symbol: String(10), Not Null, Unique. Represents the ticker symbol of the stock.
    - market: String(50), Not Null, Default: 'PSX'. Represents the market of the stock.
    - sector: String(100). Represents the sector of the stock.
    - industry: String(100). Represents the industry of the stock.
    - created_at: DateTime, Default: datetime.utcnow. Timestamp when the record was created.
    - updated_at: DateTime, Default: datetime.utcnow, onupdate: datetime.utcnow. Timestamp when the record was last updated.
    """
    __tablename__ = 'stocks'
    id = Column(Integer, Sequence('stocks_id_seq'), primary_key=True)
    asset_id = Column(Integer, nullable=False)
    ticker_symbol = Column(String(10), nullable=False, unique=True)
    market = Column(String(50), nullable=False, default='PSX')
    sector = Column(String(100))
    industry = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get(self):
        data = {
          'id': self.id,
          'asset_id': self.asset_id,
          'ticker_symbol': self.ticker_symbol,
          'market': self.market,
          'sector': self.sector,
          'industry': self.industry,
          'created_at': self.created_at,
          'updated_at': self.updated_at
        }
        return data
