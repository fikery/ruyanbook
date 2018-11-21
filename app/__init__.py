from flask import Flask
from app.models.book import db


def createApp():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    registerBlueprint(app)

    db.init_app(app)
    db.create_all(app=app)
    return app


def registerBlueprint(app):
    from app.web.book import web
    app.register_blueprint(web)