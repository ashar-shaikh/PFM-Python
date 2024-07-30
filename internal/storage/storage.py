from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from internal.storage.models import User, UserInformation


class Storage:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def check_connection(self):
        try:
            connection = self.engine.connect()
            connection.close()
            return True, None
        except Exception as e:
            return False, str(e)

    def get_session(self):
        return self.Session()
