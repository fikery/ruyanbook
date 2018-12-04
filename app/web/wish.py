from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.email import send_email
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from app.view_models.wish import MyWishes
from . import web


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    myWishes = Wish.getUserWishs(uid)
    isbnList = [wish.isbn for wish in myWishes]
    giftCountList = Wish.getGiftsNum(isbnList)
    wishViewModel = MyTrades(myWishes, giftCountList)
    return render_template('my_wish.html', wishes=wishViewModel.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.canSaveToList(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('本书已在赠送清单或者心愿清单中，请勿重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，' '请确定拥有此书，然后添加此书到赠送清单')
    else:
        send_email(wish.user.email, '有人想送你书',
                   'email/satisify_wish.html', wish=wish, gift=gift)
        flash('已发送赠送邮件，如果对方接收此书，你将获得一个烟花')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
