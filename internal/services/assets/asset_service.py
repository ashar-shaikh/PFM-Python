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

    def create_new_asset(self, ticker_symbol, country='PK',  sector='', industry=''):
        asset = Asset()
        asset.asset_symbol = ticker_symbol
        asset.asset_name = "Full Stock Name"
        asset.country = country
        asset.sector = sector
        asset.industry = industry
        _, asset_id, err = self.storage.add(asset)
        if err is not None:
            return 0, err
        return asset_id, None
