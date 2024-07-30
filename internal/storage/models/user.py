from sqlalchemy import Column, Integer, String, Sequence
from internal.storage.models.base import Base


class User(Base):
    __tablename__ = 'CardInformation'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    customer_id = Column(Integer, name='customerID')
