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

    def get_session(self):
        return self.storage.get_session()

    def add(self, instance, context=None):
        session = self.get_session()
        try:
            session.add(instance)
            session.commit()
            self.logger.info(f'Added {instance}', context)
        except Exception as e:
            session.rollback()
            self.logger.error(f'Error adding {instance}: {e}', context, exc_info=True)
        finally:
            session.close()

    def get(self, model, id=None, context=None, **kwargs):
        session = self.get_session()
        try:
            if id:
                instance = session.query(model).get(id)
                self.logger.info(f'Fetched {model.__name__} with id {id}', context)
            else:
                instance = session.query(model).filter_by(**kwargs).all()
                self.logger.info(f'Fetched {len(instance)} {model.__name__}(s) with filters {kwargs}', context)
            return instance
        except Exception as e:
            self.logger.error(f'Error fetching {model.__name__} with filters {kwargs}: {e}', context, exc_info=True)
        finally:
            session.close()

    def update(self, model, id, context=None, **kwargs):
        session = self.get_session()
        try:
            instance = session.query(model).get(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                session.commit()
                self.logger.info(f'Updated {model.__name__} with id {id}', context)
            else:
                self.logger.warning(f'No {model.__name__} found with id {id}', context)
        except Exception as e:
            session.rollback()
            self.logger.error(f'Error updating {model.__name__} with id {id}: {e}', context, exc_info=True)
        finally:
            session.close()

    def delete(self, model, id, context=None):
        session = self.get_session()
        try:
            instance = session.query(model).get(id)
            if instance:
                session.delete(instance)
                session.commit()
                self.logger.info(f'Deleted {model.__name__} with id {id}', context)
            else:
                self.logger.warning(f'No {model.__name__} found with id {id}', context)
        except Exception as e:
            session.rollback()
            self.logger.error(f'Error deleting {model.__name__} with id {id}: {e}', context, exc_info=True)
        finally:
            session.close()
