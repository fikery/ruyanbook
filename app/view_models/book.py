__author__ = 'lybin'
__date__ = '2018/11/25 12:13'


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.isbn = book['isbn']
        self.author = book['author']
        self.pages = book['pages'] or ''
        self.price = book['price']
        self.summary = book['summary'] or ''
        self.image = book['image']  # 豆瓣源需要改变
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, ruyanBook, keyword):
        self.total = ruyanBook.total
        self.books = [BookViewModel(book) for book in ruyanBook.books]
        self.keyword = keyword


class _BookViewModel:
    '''
    面向过程的伪类
    只有方法，没有数据，而对象=数据+操作数据的方法
    '''
    @classmethod
    def packageSingle(cls, data, keyWord):
        '''isbn搜索返回单条数据'''
        res = {
            'books': [],
            'total': 0,
            'keyword': keyWord
        }
        if data:
            res['total'] = 1
            res['books'] = [cls.__cutBookData(data)]

        return res

    @classmethod
    def packageCollection(cls, data, keyWord):
        '''关键字搜索返回集合'''
        res = {
            'books': [],
            'total': 0,
            'keyword': keyWord
        }
        if data:
            res['total'] = data['total']
            res['books'] = [cls.__cutBookData(book) for book in data['books']]

        return res

    @classmethod
    def __cutBookData(cls, data):
        '''对原始模型数据单条数据进行裁剪处理'''
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'author': data['author'],
            'pages': data['pages'] or '',
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']  # 豆瓣源需要改变
        }
        return book
