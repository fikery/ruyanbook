from app.libs.enums import PendingStatus

__author__ = 'lybin'
__date__ = '2018/12/3 18:54'


class FireViewModel:
    def __init__(self, fire, currentUserId):
        self.data = {}
        self.data = self._parse(fire, currentUserId)

    def _parse(self, fire, currentUserId):
        resp = self.requesterOrGifter(fire, currentUserId)
        pendingStatus = PendingStatus.pendingStr(fire.pending, resp)

        r = {
            'identify': resp,
            'fireId': fire.id,
            'bookTitle': fire.bookTitle,
            'bookAuthor': fire.bookAuthor,
            'bookImg': fire.bookImg,
            'date': fire.createDateTime.strftime('%Y-%m-%d'),
            'message': fire.message,
            'address': fire.address,
            'recipientName': fire.recipientName,
            'mobile': fire.mobile,
            'status': fire.pending,
            'operator': fire.requesterNickName if resp != 'requester' else fire.gifterNickName,
            'statusStr': pendingStatus,
        }
        return r

    @staticmethod
    def requesterOrGifter(fire, currentUserId):
        '''判断当前用户是索要者还是赠送者'''
        if currentUserId == fire.requesterId:
            resp = 'requester'
        else:
            resp = 'gifter'
        return resp


class FireCollection:
    def __init__(self, fires, currentUserId):
        self.data = []

        self._parse(fires, currentUserId)

    def _parse(self, fires, currentUserId):
        for fire in fires:
            temp = FireViewModel(fire, currentUserId)
            self.data.append(temp.data)
