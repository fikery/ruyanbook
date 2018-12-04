__author__ = 'lybin'
__date__ = '2018/11/21 22:08'


DEBUG = True  # 开启调试模式
JSON_AS_ASCII = False  # 调用flask中jsonify时正确显示中文字符串
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:mysqlpassword@localhost:3306/ruyan'
SECRET_KEY = 'myflask'

# email配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'AAA@qq.com'
MAIL_PASSWORD = '授权码'
# MAIL_SUBJECT_PREFIX = '[如烟]'
# MAIL_SENDER = '如烟Book<hello@ruyan.com>'