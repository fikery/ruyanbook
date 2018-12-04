from flask import current_app, flash, redirect, url_for, render_template

from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.fireworks import Fire
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from app.view_models.trade import MyTrades
from . import web
from flask_login import login_required, current_user


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    myGifts = Gift.getUserGifts(uid)
    isbnList = [gift.isbn for gift in myGifts]
    wishCountList = Gift.getWishesNum(isbnList)
    giftViewModel = MyTrades(myGifts, wishCountList)
    return render_template('my_gifts.html', gifts=giftViewModel.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.canSaveToList(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('本书已在赠送清单或者心愿清单中，请勿重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    fire = Fire.query.filter_by(giftId=gid, pending=PendingStatus.Waiting).first()
    if fire:
        flash('该书籍正处于交易状态，不能撤销')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
