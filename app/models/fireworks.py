from sqlalchemy import Column, Integer, String, SmallInteger

from app.libs.enums import PendingStatus
from app.models.base import Base

__author__ = 'lybin'
__date__ = '2018/12/3 16:21'


class Fire(Base):
    '''一次具体的交易信息'''
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipientName = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    bookTitle = Column(String(50))
    bookAuthor = Column(String(30))
    bookImg = Column(String(50))

    # 请求者信息
    requesterId = Column(Integer)
    requesterNickName = Column(String(20))

    # 赠送者信息
    giftId = Column(Integer)
    gifterId = Column(Integer)
    gifterNickName = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
