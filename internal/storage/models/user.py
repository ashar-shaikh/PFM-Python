from sqlalchemy import Column, Integer, String, Sequence
from internal.storage.models.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
