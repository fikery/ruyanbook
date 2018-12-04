import threading

__author__ = 'lybin'
__date__ = '2018/12/2 19:51'

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_email_async(app, msg):
    '''异步发送激活邮件'''
    with app.app_context():
        try:
            mail.send(msg)
        except:
            pass


def send_email(to, subject, template, **kwargs):
    # 测试邮件
    # msg = Message('[如烟Book]', sender='aaa@qq.com', body='Test',
    #               recipients=['user@qq.com'])
    msg = Message('[如烟Book ]' + subject, sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 传递真实的app对象，而不是current_app这个代理对象
    # 因为存在线程隔离，开启新线程异步处理后，传递current_app会找不到flask核心对象
    app = current_app._get_current_object()
    thr = threading.Thread(target=send_email_async, args=[app, msg])
    thr.start()
