from flask import Blueprint, jsonify, g
from flask import current_app as s
import internal.resources.market_data as market_data
import internal.storage.models as model

endpoint_market_summary = 'market_summary'
market_summary_bp = Blueprint(endpoint_market_summary, __name__)


@market_summary_bp.route('/' + endpoint_market_summary, methods=['GET'])
def market_summary():
    s.logger.info("Getting market summary", g.context)
    user_data = s.storage.get(model.User, 1, g.context)
    if not user_data:
        return g.server.handle_error("user not found", 0, 404, g.context)
    is_updated, updated_data = s.storage.update(model.User, 1, g.context, customer_id = 999990)
    if is_updated:
        return g.server.handle_response("{'data': 'success'}", g.context)
    stock_data = market_data.get_market_summary()
    if stock_data:
        return g.server.handle_response(stock_data, g.context)
    else:
        return g.server.handle_error("no records found", 0, 404, g.context)