from flask import jsonify, request

from app.forms.book import SearchForm
from app.libs import utils
from app.spider.ruyan_book import RuYanBook
from . import web


@web.route('/book/search')
def search():
    q = request.args['q']
    page = request.args['page']

    # 验证层
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        wordType = utils.isbnOrKey(q)
        if wordType == 'isbn':
            result = RuYanBook.searchByIsbn(q)
        else:
            result = RuYanBook.searchByKey(q)

        return jsonify(result)
    else:
        return jsonify({'msg': '参数校验失败'})
