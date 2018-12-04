__author__ = 'lybin'
__date__ = '2018/12/3 16:45'

from enum import Enum


class PendingStatus(Enum):
    '''交易状态码'''
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4

    @classmethod
    def pendingStr(cls, status, key):
        keyMap = {
            cls.Waiting: {'requester': '等待对方邮寄', 'gifter': '等待你邮寄'},
            cls.Success: {'requester': '对方已邮寄', 'gifter': '你已邮寄,交易完成'},
            cls.Reject: {'requester': '对方已拒绝', 'gifter': '你已拒绝'},
            cls.Redraw: {'requester': '对方已撤销', 'gifter': '你已撤销'},
        }
        return keyMap[status][key]
