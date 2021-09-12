import json
import os
from app import db
from app.libs.bhttp import HTTP
from app.models.book import Book


class RuYanBook:
    '''隐藏数据获取方式，只是返回数据'''
    # 模型层 MVC的M层
    # isbnUrl = 'https://api.douban.com/v2/book/isbn/{}'  # 豆瓣源
    isbnUrl = 'https://search.douban.com/book/subject_search?search_text={}'  # 豆瓣源
    keyWordUrl = 'https://search.douban.com/book/subject_search?search_text={}'
    # isbnUrl = 'http://t.yushu.im/v2/book/isbn/{}'  # 鱼书源
    # keyWordUrl = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    per_page = 15

    def __init__(self):
        self.total = 0
        self.books = []
        self.tpl = os.path.join(os.path.dirname(__file__), 'book_tpl.json')

    def searchByIsbn(self, isbn):
        # 设置缓存的思想
        book = self.query_from_mysql(isbn=isbn)
        if book:
            self.__fillSingle(book)
        else:
            url = self.isbnUrl.format(isbn)
            result = HTTP.douban_get_isbn(url)

            # with open(self.tpl, 'r') as f:
            #     result_list = json.load(f)
            # result = [x for x in result_list if isbn in x.get('isbn')]
            # result = result[0] if result else None

            self.__fillSingle(result)

            with db.auto_commit():
                book = Book()
                book.title = result['title']
                book.author = result['author']
                book.publisher = result['publisher']
                book.pubdate = result['pubdate']
                book.pages = result['pages']
                book.price = result['price']
                book.binding = result['binding']
                book.isbn = result['isbn']
                book.summary = result['summary']
                book.image = result['image']
                db.session.add(book)

    def __fillSingle(self, book):
        if book:
            self.total = 1
            self.books.append(book.get('books')[0])

    def searchByKey(self, keyWord, page):
        books = self.query_from_mysql(key=keyWord)
        if books:
            self.__fillCollection(books)
        else:
            url = self.keyWordUrl.format(keyWord, self.per_page, self.per_page * (int(page) - 1))
            result = HTTP.douban_get_key(url)
            # with open(self.tpl, 'r') as f:
            #     result_list = json.load(f)
            # books = [x for x in result_list if keyWord in x.get('title')]
            # result = {
            #     'total': len(books),
            #     'books': books
            # }
            self.__fillCollection(result)

    def __fillCollection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total > 0 else None

    @staticmethod
    def query_from_mysql(isbn=None, key=None):
        if isbn:
            book = Book.query.filter_by(isbn=isbn).first()
            books = [book]
        else:
            books = Book.query.filter(Book.title.like('%{}%'.format(key))).all()
        if not books:
            return
        # 将book对象转为dict
        book_dict_list = [{c.name: getattr(book, c.name) for c in book.__table__.columns} for book in books]
        res = {
            'total': 1,
            'books': book_dict_list
        }
        return res
