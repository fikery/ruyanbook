from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.models.base import db

login_manager = LoginManager()
mail = Mail()

def createApp():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    registerBlueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登陆网站'

    mail.init_app(app)

    db.create_all(app=app)
    return app


def registerBlueprint(app):
    from app.web.book import web
    app.register_blueprint(web)