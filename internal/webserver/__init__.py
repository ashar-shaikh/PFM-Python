from flask import Flask
import internal.webserver.routes as r
import internal.resources.helper.logger as logger
from internal.resources.helper.server import Server
from internal.application import flags

def create_app():
    db_config = {
        'db_type': 'mysql+pymysql',
        'username': flags.db_username,
        'password': flags.db_password,
        'host': flags.db_host,
        'port': flags.db_port,
        'database': flags.db_name
    }
    server = Server(__name__, r.handlers, db_config)
    return server


def app_run():
    server = create_app()
    server.run(debug=True)
    return None
