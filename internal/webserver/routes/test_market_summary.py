from flask import Blueprint, jsonify
import internal.resources.market_data as market_data

endpoint = 'market-summary'
market_summary_bp = Blueprint(endpoint, __name__)


@market_summary_bp.route('/' + endpoint, methods=['GET'])
def market_summary():
    stock_data = market_data.get_market_summary()
    if stock_data:
        return jsonify(stock_data)
    else:
        return jsonify({"error": "Failed to retrieve market data"}), 500
