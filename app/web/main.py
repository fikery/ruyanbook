from flask import render_template

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web


@web.route('/')
def index():
    recentGifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recentGifts]
    return render_template('index.html', books=books)


@web.route('/personal')
def personal_center():
    pass
