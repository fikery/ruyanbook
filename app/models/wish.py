__author__ = 'lybin'
__date__ = '2018/11/27 14:46'

from app.spider.ruyan_book import RuYanBook
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from app.models.base import Base, db
from sqlalchemy.orm import relationship


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def getUserWishs(cls, uid):
        '''根据礼物的uid号来取出用户的所有心愿'''
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.createTime)).all()
        return wishes

    @classmethod
    def getGiftsNum(cls, isbnList):
        from app.models.gift import Gift
        '''根据isbn列表到gift表中查询对应的礼物，并计算每个礼物的赠送数量'''
        countList = db.session.query(func.count(Gift.id),
                    Gift.isbn).filter(Gift.launched == False, Gift.isbn.in_(isbnList),
                    Gift.status == 1).group_by(Gift.isbn).all()
        countList = [{'count': x[0], 'isbn': x[1]} for x in countList]
        return countList

    @property
    def book(self):
        '''通过礼物的isbn，获取礼物的详细信息'''
        ruyanBook = RuYanBook()
        ruyanBook.searchByIsbn(self.isbn)
        return ruyanBook.first
