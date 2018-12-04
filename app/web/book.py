import json

from flask import request, jsonify, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs import utils
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.ruyan_book import RuYanBook
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    '''视图函数，返回json格式API结果'''
    books = BookCollection()
    form = SearchForm(request.args)
    # 验证层
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        wordType = utils.isbnOrKey(q)

        if wordType == 'isbn':
            ruyanBook = RuYanBook()
            ruyanBook.searchByIsbn(q)
        else:
            ruyanBook = RuYanBook()
            ruyanBook.searchByKey(q, page)

        books.fill(ruyanBook, q)
        # return json.dumps(books, ensure_ascii=False, default=lambda x: x.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    hasInGifts = False
    hasInWishes = False

    # 取出书籍的详情数据
    ruyanBook = RuYanBook()
    ruyanBook.searchByIsbn(isbn)
    book = BookViewModel(ruyanBook.first)

    # 判断是否登陆
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            hasInGifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            hasInWishes = True

    tradeGifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    tradeWishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    tradeGiftsModel = TradeInfo(tradeGifts)
    tradeWishesModel = TradeInfo(tradeWishes)

    return render_template('book_detail.html', book=book, wishes=tradeWishesModel, gifts=tradeGiftsModel,
                           hasInGifts=hasInGifts, hasInWishes=hasInWishes)


@web.route('/test')
def test():
    r = {
        'name': 'abc',
        'age': 7
    }
    flash('OK,baby', category='warning')
    flash('NO,baby', category='error')
    return render_template('test.html', data=r)