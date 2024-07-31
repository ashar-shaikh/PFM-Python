from internal.storage.storage import Storage
from internal.resources.helper.logger import LoggerManager

class DatabaseManager:
    def __init__(self, db_type, username, password, host, port, database):
        # Raise Error in case of missing values
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
            self.rollback_session()
        else:
            self.commit_session()
        self.close_session()

    def check_connection(self):
        return self.storage.check_connection()

    def get_session(self):
        if self.session is None or not self.session.is_active:
            self.session = self.storage.get_session()
            self.logger.info('Created a new database session')
        return self.session

    def commit_session(self, context=None):
        try:
            if self.session:
                self.session.commit()
                self.logger.info('Committed the database session', context)
        except Exception as e:
            self.logger.error(f'Error committing the session: {e}', context, exc_info=True)
            self.rollback_session(context)

    def rollback_session(self, context=None):
        try:
            if self.session:
                self.session.rollback()
                self.logger.info('Rolled back the database session', context)
        except Exception as e:
            self.logger.error(f'Error rolling back the session: {e}', context, exc_info=True)

    def close_session(self, context=None):
        try:
            if self.session:
                self.session.close()
                self.session = None
                self.logger.info('Closed the database session', context)
        except Exception as e:
            self.logger.error(f'Error closing the session: {e}', context, exc_info=True)

    def add(self, instance, context=None, session=None):
        local_session = False
        if session is None:
            session = self.get_session()
            local_session = True
        try:
            session.add(instance)
            self.logger.info(f'Added {instance}', context)
            if local_session:
                session.commit()
            return True, None
        except Exception as e:
            if local_session:
                session.rollback()
            self.logger.error(f'Error adding {instance}: {e}', context, exc_info=True)
            return False, f'Error adding {instance}: {e}'
        finally:
            if local_session:
                self.close_session(context)

    def get(self, model, id=None, context=None, session=None, **kwargs):
        local_session = False
        if session is None:
            session = self.get_session()
            local_session = True
        try:
            if id:
                instance = session.query(model).get(id)
                self.logger.info(f'Fetched {model.__name__} with id {id}', context)
            else:
                instance = session.query(model).filter_by(**kwargs).all()
                self.logger.info(f'Fetched {len(instance)} {model.__name__}(s) with filters {kwargs}', context)
            return instance, None
        except Exception as e:
            self.logger.error(f'Error fetching {model.__name__} with filters {kwargs}: {e}', context, exc_info=True)
            return None, f'Error fetching {model.__name__} with filters {kwargs}: {e}'
        finally:
            if local_session:
                self.close_session(context)

    def get_list(self, model_class, context=None, session=None, limit=None, **kwargs):
        local_session = False
        if session is None:
            session = self.get_session()
            local_session = True
        try:
            query = session.query(model_class).filter_by(**kwargs)
            if limit:
                query = query.limit(limit)
            instances = query.all()
            self.logger.info(f'Fetched {len(instances)} {model_class.__name__}(s) with filters {kwargs}', context)
            return instances
        except Exception as e:
            self.logger.error(f'Error fetching list of {model_class.__name__} with filters {kwargs}: {e}', context, exc_info=True)
            return []
        finally:
            if local_session:
                self.close_session(context)

    def update(self, model, id, context=None, session=None, **kwargs):
        local_session = False
        if session is None:
            session = self.get_session()
            local_session = True
        try:
            instance = session.query(model).get(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                self.logger.info(f'Updated {model.__name__} with id {id}', context)
                if local_session:
                    session.commit()
                return True, instance
            else:
                self.logger.warning(f'No {model.__name__} found with id {id}', context)
                return False, None
        except Exception as e:
            if local_session:
                session.rollback()
            self.logger.error(f'Error updating {model.__name__} with id {id}: {e}', context, exc_info=True)
            return False, None
        finally:
            if local_session:
                self.close_session(context)

    def delete(self, model, id, context=None, session=None):
        local_session = False
        if session is None:
            session = self.get_session()
            local_session = True
        try:
            instance = session.query(model).get(id)
            if instance:
                session.delete(instance)
                self.logger.info(f'Deleted {model.__name__} with id {id}', context)
                if local_session:
                    session.commit()
                return True
            else:
                self.logger.warning(f'No {model.__name__} found with id {id}', context)
                return False
        except Exception as e:
            if local_session:
                session.rollback()
            self.logger.error(f'Error deleting {model.__name__} with id {id}: {e}', context, exc_info=True)
            return False
        finally:
            if local_session:
                self.close_session(context)
