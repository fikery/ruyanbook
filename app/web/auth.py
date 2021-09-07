from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from app.libs.email import send_email
from app.models.base import db
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.user import User
from . import web


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.setAttrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email= form.email.data).first()
        if user and user.checkPassword(form.password.data):
            login_user(user, remember=True)
            nextUrl = request.args.get('next')
            if not nextUrl or not nextUrl.startswith('/'):
                nextUrl = url_for('web.index')
            return redirect(nextUrl)
        else:
            flash('账号不存在或者密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            accountEmail = form.email.data
            user = User.query.filter_by(email=accountEmail).first_or_404()
            send_email(form.email.data, '重置密码', 'email/reset_password.html',
                       user=user, token=user.generateToken())
            flash('激活邮件已经发送到邮箱'+accountEmail+', 请及时验证')

    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.resetPassword(token, form.password1.data)
        if success:
            flash('密码更新成功，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    return render_template('auth/change_password.html')


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
