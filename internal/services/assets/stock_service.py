from internal.storage.models.assets.stock import Stock
from internal.storage.models.assets.asset import Asset
from internal.services.assets.asset_service import AssetService
from internal.resources.assets.market_data.psx_data import PSXData


class StockService:
    def __init__(self, storage, context, session, logger):
        self.storage = storage
        self.context = context
        self.session = session
        self.logger = logger
        self.AssetService = AssetService(storage, context, session, logger)
        self.psx = PSXData()

    @staticmethod
    def lookup_stock_symbols():
        try:
            stock_data = PSXData().get_market_summary()
            stock_symbols = stock_data["data"].keys()
            return stock_symbols, None
        except Exception as e:
            err = f"Error fetching stock symbols: {repr(e)}"
            return None, err

    def create_new_stock(self, asset_id, country='PK', market='PSX', sector='',  ticker_symbol=''):
        stock = Stock()
        stock.asset_id = asset_id
        stock.country = country
        stock.market = market
        stock.sector = sector
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
            stock_data, err = self.clean_existing_stocks(stock_data)
            if err is not None:
                return 0, [], err

            asset_data, err = self.AssetService.clean_existing_assets(stock_data)
            if asset_data is None:
                return 0, [], err
            for stock_symbol in stock_data:
                if len(stock_ids) >= limit:
                    break

                company_data, error = self.psx.get_company_data(stock_symbol)
                if error:
                    return 0, [], error
                # Identify and Save new Assets for PK
                asset_exists = True if stock_symbol in asset_data.keys() else False
                if not asset_exists:
                    asset_id, err = self.AssetService.create_new_asset(stock_symbol,
                                                                       name=company_data['Company Name'],
                                                                       description=company_data['description'],
                                                                       currency='PKR')
                    if err is not None:
                        return 0, [], err
                else:
                    asset_id = asset_data[stock_symbol]

                if len(stock_data) > 0:
                    continue

                # Identify and Save new Stocks for PK
                stock_id, err = self.create_new_stock(asset_id,
                                                      ticker_symbol=stock_symbol,
                                                      sector=company_data['Sector'],
                                                      country='PK')
                if err is not None:
                    continue
                stock_ids.append(stock_id)

            # Return Stock Count and Stock IDs
            return len(stock_ids), stock_ids, None
        except Exception as e:
            err = f"Error creating new stocks: {repr(e)}"
            return 0, [], err

    def clean_existing_stocks(self, existing_stocks):
        try:
            stock_data = self.storage.fetch_all(
                model_class=Stock,
                filters={'ticker_symbol': existing_stocks}
            )
            for stock in stock_data:
                if stock.ticker_symbol in existing_stocks:
                    existing_stocks.remove(stock.ticker_symbol)
            return existing_stocks, None
        except Exception as e:
            err = f"Error fetching existing stocks: {repr(e)}"
            return None, err

    # TODO: Update Live Stock Data to the Live Price Table
    # TODO: Update Daily Position to the Daily Position Table
