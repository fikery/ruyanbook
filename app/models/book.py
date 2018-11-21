__author__ = 'lybin'
__date__ = '2018/11/21 21:50'
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='译名')
    isbn = Column(String(15), nullable=False, unique=True)
    publisher = Column(String(20))
    price = Column(String(20))
    pages = Column(Integer)
    binding = Column(String(20))
    pubdate = Column(String(20))
    summary = Column(String(1000))
    image = Column(String(50))