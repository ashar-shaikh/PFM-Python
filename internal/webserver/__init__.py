from flask import Flask
import internal.webserver.routes as r
import internal.resources.helper.logger as logger
from internal.resources.helper.server import Server


def create_app():
    db_config = {
        'db_type': 'mysql+pymysql',
        'username': 'admin',
        'password': '',
        'host': 'localhost',
        'port': '',
        'database': 'example.db'
    }
    server = Server(__name__, r.handlers, db_config)
    return server


def app_run():
    server = create_app()
    server.run(debug=True)
    return None
