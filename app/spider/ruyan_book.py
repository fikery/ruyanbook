from app.libs.bhttp import HTTP


class RuYanBook:
    # isbnUrl = 'https://api.douban.com/v2/book/isbn/{}'
    isbnUrl = 'http://t.yushu.im/v2/book/isbn/{}'
    keyWordUrl = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def searchByIsbn(cls, isbn):
        url = cls.isbnUrl.format(isbn)
        result = HTTP.get(url)
        return result

    @classmethod
    def searchByKey(cls, keyWord, count=15, start=0):
        url = cls.keyWordUrl.format(keyWord, count, start)
        result = HTTP.get(url)
        return result