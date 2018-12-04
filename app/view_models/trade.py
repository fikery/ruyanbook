__author__ = 'lybin'
__date__ = '2018/11/28 21:02'

from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__mapToTrade(single) for single in goods]

    def __mapToTrade(self, single):
        if single.createDateTime:
            creTime = single.createDateTime.strftime('%Y-%m-%d')
        else:
            creTime = '未知'

        return dict(
            userName=single.user.nickName,
            creTime=creTime,
            id=single.id
        )


class MyTrades:
    def __init__(self, myTrades, tradeCountList):
        self.trades = []
        self._myTrades = myTrades
        self._tradeCountList = tradeCountList
        self.trades = self._parse()

    def _parse(self):
        tempList = []
        for trade in self._myTrades:
            mytrade = self._matching(trade)
            tempList.append(mytrade)
        return tempList

    def _matching(self, trade):
        count = 0
        for tradeCount in self._tradeCountList:
            if trade.isbn == tradeCount['isbn']:
                count = tradeCount['count']

        r = {
            'tradesCount': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }
        return r
