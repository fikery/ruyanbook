from flask import render_template
from flask_login import current_user

from app.models.gift import Gift
from app.models.user import get_user
from app.view_models.book import BookViewModel
from . import web


@web.route('/')
def index():
    recentGifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recentGifts]
    return render_template('index.html', books=books)


@web.route('/personal')
def personal_center():
    user = get_user(current_user.id)
    return render_template('personal.html', user=user.summary)
