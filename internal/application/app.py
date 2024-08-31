import internal.webserver.routes as r
from internal.resources.generic.helper.server import Server
from internal.application import flags


class App:
    def __init__(self, name):
        db_config = {
            'db_type': 'mysql+pymysql',
            'username': flags.db_username,
            'password': flags.db_password,
            'host': flags.db_host,
            'port': flags.db_port,
            'database': flags.db_name
        }
        self.server = Server(name, r.handlers, db_config)

    def run(self):
        self.server.run(debug=True)
        return None
