from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from internal.storage.models.base import Base


class UserInformation(Base):
    __tablename__ = 'user_information'
    id = Column(Integer, Sequence('user_info_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    information = Column(String(100))
