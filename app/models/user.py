from flask import current_app
from math import floor

from app.libs.enums import PendingStatus
from app.models.fireworks import Fire

__author__ = 'lybin'
__date__ = '2018/11/26 17:39'

from app.libs.utils import isbnOrKey
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.ruyan_book import RuYanBook

from sqlalchemy import Column, Integer, String, Boolean, Float
from app.models.base import Base, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, Base):
    # __tablename__ = 'user1'  # 修改表名
    id = Column(Integer, primary_key=True)
    nickName = Column(String(24), nullable=False)
    phoneNumber = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    sendCounter = Column(Integer, default=0)
    receiveCounter = Column(Integer, default=0)
    wxOpenId = Column(String(50))
    wxName = Column(String(32))
    _password = Column('password', String(128), nullable=False)  # 指定字段名

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def checkPassword(self, raw):
        return check_password_hash(self._password, raw)

    def canSaveToList(self, isbn):
        '''
        检查礼物是否是isbn编号
        是否在数据源中
        是否同时多次赠送
        是否同时赠送又索要
        '''
        if isbnOrKey(isbn) != 'isbn':
            return False
        ruyanBook = RuYanBook()
        ruyanBook.searchByIsbn(isbn)
        if not ruyanBook.first:
            return False
        # 既不在赠送清单中也不在心愿清单中，才可以添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generateToken(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def resetPassword(token, newPassword):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            if user:
                user.password = newPassword
            else:
                return False
        return True

    def canSendFireworks(self):
        '''判断积分是否允许获取赠送书籍'''
        if self.beans < 1:
            return False
        # 成功赠送的书籍数量
        successGiftsCount = Gift.query.filter_by(uid=self.id,
                                                 launched=True).count()
        # 成功索要的书籍数量
        successReceiveCount = Fire.query.filter_by(requesterId=self.id,
                                                   pending=PendingStatus.Success).count()
        # 每赠送2本书籍，才能索要一本书籍
        return True if \
            floor(successReceiveCount / 2) <= floor(successGiftsCount)\
            else False

    @property
    def summary(self):
        '''用户简介'''
        return dict(
            nickName=self.nickName,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.sendCounter) + '/' + str(self.receiveCounter)
        )


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
