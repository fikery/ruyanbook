from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForm(Form):
    q = StringField(validators=[Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class FireForm(Form):
    recipientName = StringField(
        validators=[DataRequired('请输入收件人名称'),
                    Length(min=2, max=20, message='收件人姓名长度在2-20位之间')])
    mobile = StringField(validators=[DataRequired(),
                                     Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号码')])
    message = StringField()
    address = StringField(validators=[DataRequired(),
                                      Length(10, 70, '地址长度在10到70个位之间')])
