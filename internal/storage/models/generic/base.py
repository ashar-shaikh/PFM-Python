from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import declared_attr
import datetime



@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def get(self):
        data = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                data[key] = getattr(self, key)
        data['__name__'] = self.__class__.__name__
        return data

    def __repr__(self):
        return f'<{self.__class__.__name__} {getattr(self, "id")}>'
