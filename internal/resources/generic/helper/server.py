import uuid
from flask import Flask, request, g, jsonify

from internal.resources.generic.helper.database import DatabaseManager
from internal.resources.generic.helper.logger import LoggerManager
from internal.resources.generic.helper.context import Context


class Server:
    def __init__(self, name, routes, db_config, port=5000):
        self.app = Flask(name)
        self.logger = LoggerManager(name)
        self.routes = routes
        self.db_manager = DatabaseManager(**db_config)
        self.port = port

    def middleware(self):
        @self.app.before_request
        def before_request():
            # Create a trace ID and context
            trace_id = request.headers.get('X-Trace-ID', str(uuid.uuid4()))
            g.context = Context(trace_id=trace_id)
            g.server = self
            # Add security checks here
            endpoint = request.endpoint
            route_config = self.routes.get(endpoint, {})
            secure = route_config.get("secure", False)
            if secure:
                api_key = request.headers.get('X-API-KEY')
                if not api_key or api_key != 'expected_api_key':
                    return 'Unauthorized', 401

            # Log the request details
            self.logger.info("Request received", context=g.context, method=request.method, path=request.path)

        @self.app.after_request
        def after_request(response):
            return response

    def add_routes(self):
        for route, config in self.routes.items():
            blueprint = config["blueprint"]
            self.app.register_blueprint(blueprint)

    def handle_response(self, body, context=None, status_code=200):
        response = {
            "success": True,
            "data": body,
        }
        self.logger.info("Response generated", context=context, response=response)
        return jsonify(response), status_code

    def handle_error(self, message, error_code, status_code=400, context=None):
        response = {
            "success": False,
            "error": {
                "code": error_code,
                "message": message
            },
        }
        self.logger.error("Error response generated", context=context, response=response)
        return jsonify(response), status_code

    def check_db_connection(self):
        connected, error = self.db_manager.check_connection()
        if not connected:
            self.logger.error(f"Failed to connect to the database: {error}")
            raise Exception(f"Failed to connect to the database: {error}")
        self.logger.info("Database connection successful")

    def run(self, **kwargs):
        self.middleware()
        self.add_routes()
        # noinspection PyPropertyAccess
        self.app.logger = self.logger
        # noinspection PyPropertyAccess
        self.app.storage = self.db_manager
        self.check_db_connection()
        self.logger.info("Starting Flask Server", context=None, port=self.port)
        self.app.run(**kwargs)
