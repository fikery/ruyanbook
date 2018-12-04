from app.view_models.book import BookViewModel

__author__ = 'lybin'
__date__ = '2018/12/1 20:45'


class MyGifts:
    def __init__(self, myGifts, wishCountList):
        self.gifts = []
        self._myGifts = myGifts
        self._wishCountList = wishCountList
        self.gifts = self._parse()

    def _parse(self):
        tempList = []
        for gift in self._myGifts:
            mygift = self._matching(gift)
            tempList.append(mygift)
        return tempList

    def _matching(self, gift):
        count = 0
        for wishGift in self._wishCountList:
            if gift.isbn == wishGift['isbn']:
                count = wishGift['count']

        r = {
            'wishesCount': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return r
