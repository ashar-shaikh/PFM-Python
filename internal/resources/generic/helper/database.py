from internal.storage.storage import Storage
from internal.resources.generic.helper.logger import LoggerManager

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

    def fetch_all(self, model_class, limit=None, offset=None, filters=None, order_by=None, session=None, context=None):
        """
        Fetches all records for a given model class with optional limits, offsets, and filters.

        :param model_class: The ORM model class to fetch data from.
        :param limit: The maximum number of records to return.
        :param offset: The number of records to skip before starting to return records.
        :param filters: A dictionary of filters to apply to the query.
        :param order_by: The field by which to order the results.
        :param session: Optional session object if already within a session context.
        :param context: Optional context for logging.
        :return: A list of records fetched from the database.
        """
        session_provided = session is not None
        session = session or self.get_session()
        try:
            query = session.query(model_class)

            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(model_class, key) == value)

            if order_by:
                query = query.order_by(order_by)

            if limit:
                query = query.limit(limit)

            if offset:
                query = query.offset(offset)

            result = query.all()
            self.logger.info(f'Fetched {len(result)} records from {model_class.__name__}', context)
            return result
        except Exception as e:
            self.logger.error(f'Error fetching records from {model_class.__name__}: {e}', context, exc_info=True)
            raise
        finally:
            if not session_provided:
                self.close_session(session, context)
                