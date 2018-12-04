__author__ = 'lybin'
__date__ = '2018/11/26 17:40'

from flask import current_app
from app.spider.ruyan_book import RuYanBook
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from app.models.base import Base, db
from sqlalchemy.orm import relationship


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    def isYourselfGift(self, uid):
        '''判断当前gift是否是自己的'''
        return True if self.user.id == uid else False

    @classmethod
    def getUserGifts(cls, uid):
        '''根据礼物的uid号来取出用户的所有礼物'''
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.createTime)).all()
        return gifts

    @classmethod
    def getWishesNum(cls, isbnList):
        from app.models.wish import Wish
        '''根据isbn列表到wish表中查询对应的礼物，并计算每个礼物的心愿数量'''
        countList = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                Wish.isbn.in_(isbnList), Wish.status==1).group_by(Wish.isbn).all()
        countList = [{'count': x[0], 'isbn': x[1]} for x in countList]
        return countList

    # 这里之所以采用类方法主要是因为，Gift实例是指一条礼物数据，在一条数据中查询多条数据是不符合逻辑的
    # 而类则是代表礼物的抽象，不是具体的单条数据，因此可以对类对象进行查询多条数据
    @classmethod
    def recent(cls):
        '''查询最近赠送的不重复的30本书籍'''
        recentGift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.createTime)).limit(
            current_app.config['RECENT_COUNT']).distinct().all()
        return recentGift

    @property
    def book(self):
        '''通过礼物的isbn，获取礼物的详细信息'''
        ruyanBook = RuYanBook()
        ruyanBook.searchByIsbn(self.isbn)
        return ruyanBook.first
