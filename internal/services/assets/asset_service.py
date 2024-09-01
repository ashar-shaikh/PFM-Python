from internal.storage.models.assets.asset import Asset


class AssetService:
    def __init__(self, storage, context, session, logger):
        self.storage = storage
        self.context = context
        self.session = session
        self.logger = logger

    def lookup_asset_name(self, ticker_symbol, asset_type='stock', country='PK'):
        try:
            existing_assets = self.storage.fetch_all(
                                    model_class=Asset,
                                    limit=1,
                                    filters={'asset_symbol': ticker_symbol,
                                             'asset_type': asset_type,
                                             'country': country},
                                )
            if len(existing_assets) > 0:
                existing_asset = existing_assets[0]
                return True, existing_asset.get()['id'], None
            return False, None, None
        except Exception as e:
            err = f"Error looking up asset: {repr(e)}"
            return None, None, err

    def create_new_asset(self, ticker_symbol, name='', description='', currency='', country='PK'):
        asset = Asset()
        asset.asset_name = name
        asset.asset_symbol = ticker_symbol
        asset.country = country
        asset.currency = currency
        asset.description = description

        _, asset_id, err = self.storage.add(asset)
        if err:
            return 0, err
        if asset_id is None:
            return 0, "Failed to create asset"
        return asset_id, None

    def clean_existing_assets(self, existing_stocks):
        try:
            asset_data = self.storage.fetch_all(
                model_class=Asset,
                filters={'asset_symbol': existing_stocks,
                         'asset_type': 'stock',
                         'country': 'PK'}
            )
            resp_data = {}

            for asset in asset_data:
                if asset.asset_symbol not in existing_stocks:
                    resp_data[asset.asset_symbol] = asset.id
            return existing_stocks, None
        except Exception as e:
            err = f"Error fetching existing stocks: {repr(e)}"
            return None, err
