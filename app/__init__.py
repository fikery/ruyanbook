from flask import Flask


def createApp():
    app = Flask(__name__)
    app.config.from_object('config')
    registerBlueprint(app)
    return app


def registerBlueprint(app):
    from app.web.book import web
    app.register_blueprint(web)