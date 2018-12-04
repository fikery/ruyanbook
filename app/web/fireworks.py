from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc, or_

from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.models.base import db
from app.forms.book import FireForm
from app.models.fireworks import Fire
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.fireworks import FireCollection
from . import web


@web.route('/fire/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_fire(gid):
    # 获取当前赠送的书籍
    currentGift = Gift.query.get_or_404(gid)
    # 判断是否向自己索要书籍
    if currentGift.isYourselfGift(current_user.id):
        flash('不能向自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=currentGift.isbn))
    # 判断积分是否符合索要书籍的条件
    can = current_user.canSendFireworks()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    # 提交索要表单
    form = FireForm(request.form)
    if request.method == 'POST' and form.validate():
        save_fireworks(form, currentGift)
        # 发送邮件通知
        # send_email(currentGift.user.email, '有人想要书',
        #            'email/get_gift.html', wisher=current_user, gift=currentGift)
        return redirect(url_for('web.pending'))

    # 获取当前书籍拥有者的简介
    gifter = currentGift.user.summary
    return render_template('fireworks.html', gifter=gifter,
                           userBeans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    fires = Fire.query.filter(
        or_(Fire.requesterId == current_user.id, Fire.gifterId == current_user.id)).order_by(
        desc(Fire.createTime)
    ).all()

    views = FireCollection(fires, current_user.id)

    return render_template('pending.html', fires=views.data)


@web.route('/fire/<int:fid>/reject')
@login_required
def reject_fire(fid):
    with db.auto_commit():
        fire = Fire.query.filter(Gift.uid == current_user.id, Fire.id == fid).first_or_404()
        # 变更礼物的状态
        fire.pending = PendingStatus.Reject
        # 退还积分
        requester = User.query.get_or_404(fire.requesterId)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/fire/<int:fid>/redraw')
@login_required
def redraw_fire(fid):
    with db.auto_commit():
        fire = Fire.query.filter(Fire.requesterId == current_user.id, Fire.id == fid).first_or_404()
        fire.pending = PendingStatus.Redraw
        # 退还积分
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/fire/<int:fid>/mailed')
@login_required
def mailed_fire(fid):
    '''已邮寄，完成交易'''
    with db.auto_commit():
        fire = Fire.query.filter_by(id=fid, gifterId=current_user.id).first_or_404()
        fire.pending = PendingStatus.Success
        # 奖励积分
        current_user.beans += 1
        # 更新礼物赠送状态
        gift = Gift.query.filter_by(id=fire.giftId).first_or_404()
        gift.launched = True
        # # 更新心愿状态
        wish = Wish.query.filter_by(isbn=fire.isbn).first_or_404()
        wish.launched = True

        # 单条更新语句
        # gift = Gift.query.filter_by(id=fire.giftId, uid=fire.requesterId,
        #                             launched=False).update({'Wish.launched:True'})
    return redirect(url_for('web.pending'))


def save_fireworks(fireForm, currentGift):
    with db.auto_commit():
        fire = Fire()
        # wtforms提供自动直接赋值,两个对象的各个字段名称要一致
        fireForm.populate_obj(fire)
        # 礼物的赠送与索要者信息
        fire.giftId = currentGift.id
        fire.requesterId = current_user.id
        fire.requesterNickName = current_user.nickName
        fire.gifterId = currentGift.user.id
        fire.gifterNickName = currentGift.user.nickName
        # 礼物的书籍信息
        book = BookViewModel(currentGift.book)
        fire.bookTitle = book.title
        fire.bookAuthor = book.author
        fire.bookImg = book.image
        fire.isbn = book.isbn
        # 积分-1
        current_user.beans -= 1
        db.session.add(fire)
