from flask import Blueprint, g, request
from flask import current_app as s
from internal.services.assets.stock_service import StockService

endpoint_add_stocks = 'add_stocks'
add_stocks_bp = Blueprint(endpoint_add_stocks, __name__)


@add_stocks_bp.route('/' + endpoint_add_stocks, methods=['POST'])
def add_stocks():
    ctx = g.context
    storage = s.storage
    with storage as session:
        try:
            s.logger.info("Fetching and Saving New Stocks", g.context)
            # Get limit from request
            limit = request.args.get('limit', 1)
            limit = int(limit)
            # Create an instance of StockService with the current session, context, and storage
            stock_service = StockService(storage=storage, context=ctx, session=session, logger=s.logger)
            stock_count, stock_ids, err = stock_service.create_new_stocks(limit)
            if err is not None:
                return g.server.handle_error(err, 0, 500, ctx)
            result = {
                'count': stock_count,
                'IDs': stock_ids
            }
            return g.server.handle_response(result, ctx)
        except Exception as e:
            return g.server.handle_error(repr(e), 0, 500, ctx)

