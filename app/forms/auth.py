from app.models.user import User

__author__ = 'lybin'
__date__ = '2018/11/26 20:37'

from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo


class RegisterForm(Form):
    '''注册表单验证'''
    nickName = StringField(validators=[DataRequired(message='昵称不能为空'), Length(2, 10, message='昵称字符数最少2位，最多10位')])
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Length(8, 64), Email(message='邮箱格式错误')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_nickName(self, field):
        if User.query.filter_by(nickName=field.data).first():
            raise ValidationError('昵称已经被注册')


class LoginForm(Form):
    '''登录表单验证'''
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Length(8, 64), Email(message='邮箱格式错误')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(message='邮箱不能为空'), Length(8, 64), Email(message='邮箱格式错误')])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='密码长度需在6-32位之间'),
        EqualTo('password2', message='两次输入密码不一致')
    ])
    password2 = PasswordField(validators=[DataRequired(), Length(6, 32)])
