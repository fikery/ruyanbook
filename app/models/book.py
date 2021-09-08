__author__ = 'lybin'
__date__ = '2018/11/21 21:50'

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='佚名')
    isbn = Column(String(15), nullable=False, unique=True)
    publisher = Column(String(20))
    price = Column(String(20))
    pages = Column(Integer)
    binding = Column(String(20))
    pubdate = Column(String(20))
    summary = Column(String(1000))
    image = Column(String(250))
