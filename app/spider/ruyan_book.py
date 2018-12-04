from app.libs.bhttp import HTTP


class RuYanBook:
    '''隐藏数据获取方式，只是返回数据'''
    # 模型层 MVC的M层
    # isbnUrl = 'https://api.douban.com/v2/book/isbn/{}'  # 豆瓣源
    isbnUrl = 'http://t.yushu.im/v2/book/isbn/{}'  # 鱼书源
    keyWordUrl = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    per_page = 15

    def __init__(self):
        self.total = 0
        self.books = []

    def searchByIsbn(self, isbn):
        url = self.isbnUrl.format(isbn)
        result = HTTP.get(url)
        self.__fillSingle(result)

        # 设置缓存的思想
        # book = query_from_mysql(isbn)
        # if book:
        #     return book
        # else:
        #     save(result)

    def __fillSingle(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def searchByKey(self, keyWord, page):
        url = self.keyWordUrl.format(keyWord, self.per_page, self.per_page*(int(page)-1))
        result = HTTP.get(url)
        self.__fillCollection(result)

    def __fillCollection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total > 0 else None