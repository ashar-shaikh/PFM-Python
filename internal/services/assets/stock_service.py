from internal.storage.models.assets.stock import Stock
from internal.storage.models.assets.asset import Asset
from internal.services.assets.asset_service import AssetService
from internal.resources.assets.market_data.psx_data import MarketSummary


class StockService:
    def __init__(self, storage, context, session, logger):
        self.storage = storage
        self.context = context
        self.session = session
        self.logger = logger
        self.AssetService = AssetService(storage, context, session, logger)

    @staticmethod
    def lookup_stock_symbols():
        try:
            stock_data = MarketSummary().get_market_summary()
            stock_symbols = stock_data["data"].keys()
            return stock_symbols, None
        except Exception as e:
            err = f"Error fetching stock symbols: {repr(e)}"
            return None, err

    def create_new_stock(self, asset_id, country='PK', market='PSX', sector='', industry='', ticker_symbol=''):
        stock = Stock()
        stock.asset_id = asset_id
        stock.country = country
        stock.market = market
        stock.sector = sector
        stock.industry = industry
        stock.ticker_symbol = ticker_symbol
        _, stock_id, err = self.storage.add(stock)
        if err is not None:
            return 0, err
        return stock_id, None

    # Create New Stocks
    def create_new_stocks(self, limit=100):
        try:
            stock_ids = []
            stock_data, err = self.lookup_stock_symbols()
            if err is not None:
                return 0, [], err
            for stock_symbol in stock_data:
                if len(stock_ids) >= limit:
                    break

                # Identify and Save new Assets for PK
                asset_exists, asset_id, err = self.AssetService.lookup_asset_name(stock_symbol)
                if err is not None:
                    return 0, [], err
                if not asset_exists:
                    # TODO: Look up stock details
                    asset_id, err = self.AssetService.create_new_asset(stock_symbol)
                    if err is not None:
                        return 0, [], err
                # Check Asset ID to see if Stock already exists
                stock_data = self.storage.fetch_all(
                    model_class=Stock,
                    limit=1,
                    filters={'asset_id': asset_id}
                )
                if len(stock_data) > 0:
                    continue

                # Identify and Save new Stocks for PK
                stock_id, err = self.create_new_stock(asset_id, ticker_symbol=stock_symbol)
                if err is not None:
                    continue
                stock_ids.append(stock_id)

            # Return Stock Count and Stock IDs
            return len(stock_ids), stock_ids, None
        except Exception as e:
            err = f"Error creating new stocks: {repr(e)}"
            return 0, [], err

    # TODO: Update Live Stock Data to the Live Price Table
    # TODO: Update Daily Position to the Daily Position Table
