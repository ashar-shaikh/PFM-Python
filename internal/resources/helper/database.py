from sqlalchemy.orm import joinedload
from internal.storage.storage import Storage
from internal.resources.helper.logger import LoggerManager

class DatabaseManager:
    def __init__(self, db_type, username, password, host, port, database):
        if not all([username, host, database]):
            raise ValueError("Database configuration missing values")
        if not db_type:
            db_type = 'mysql+mysqlclient'
        if not port:
            port = 3306
        db_url = f"{db_type}://{username}:{password}@{host}:{port}/{database}"
        self.storage = Storage(db_url)
        self.logger = LoggerManager('DatabaseManager').logger
        self.session = None

    def __enter__(self):
        self.session = self.get_session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type or exc_value or traceback:
            self.rollback_session(self.session)
        else:
            self.commit_session(self.session)
        self.close_session(self.session)

    def check_connection(self):
        return self.storage.check_connection()

    def get_session(self):
        return self.storage.get_session()

    def commit_session(self, session, context=None):
        try:
            session.commit()
            self.logger.info('Committed the database session', context)
        except Exception as e:
            self.logger.error(f'Error committing the session: {e}', context, exc_info=True)
            session.rollback()

    def rollback_session(self, session, context=None):
        try:
            session.rollback()
            self.logger.info('Rolled back the database session', context)
        except Exception as e:
            self.logger.error(f'Error rolling back the session: {e}', context, exc_info=True)

    def close_session(self, session, context=None):
        try:
            session.close()
            self.logger.info('Closed the database session', context)
        except Exception as e:
            self.logger.error(f'Error closing the session: {e}', context, exc_info=True)

    def execute(self, func, *args, **kwargs):
        session_provided = 'session' in kwargs and kwargs['session'] is not None
        session = kwargs.pop('session', None) or self.get_session()
        context = kwargs.pop('context', None)
        try:
            result = func(session, *args, **kwargs)
            if not session_provided:
                self.commit_session(session, context)
            self.logger.info(f'Executed {func.__name__}', context)
            return result
        except Exception as e:
            if not session_provided:
                self.rollback_session(session, context)
            self.logger.error(f'Error executing {func.__name__}: {e}', context, exc_info=True)
            raise
        finally:
            if not session_provided:
                self.close_session(session, context)

    def add(self, instance, context=None, session=None):
        session_provided = session is not None
        session = session or self.get_session()
        try:
            session.add(instance)
            if not session_provided:
                self.commit_session(session, context)
            self.logger.info(f'Added {instance}', context)
            return True, instance.id, None  # Assuming 'id' is the primary key field
        except Exception as e:
            if not session_provided:
                self.rollback_session(session, context)
            self.logger.error(f'Error adding {instance}: {e}', context, exc_info=True)
            return False, None, f'Error adding {instance}: {e}'
        finally:
            if not session_provided:
                self.close_session(session, context)
