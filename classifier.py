# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
    分类器, 对于每一个email, 单独调用类去判别, 输出所属的分类
'''

import spacy
from spacy.matcher import Matcher
from spacy.attrs import LOWER

from enum import IntEnum

class Category(IntEnum):
    conversation = 1
    order_shipping = 2
    order_acknowledgement = 3
    finance = 4
    others = -1


class BaseClassifier(object):
    '''
        分类器的公共基类, 用来处理统一的,共有的操作
        并且用公共类的方式标注出 接口
    '''

    def category(self):
        raise NotImplementedError()


class ReClassifier(BaseClassifier):
    '''
        正则版本
    '''
    def category(self, email):
        '''
            测试, 不管怎么样 返回一个 对话类
        '''
        return Category.conversation



class SpacyClassifier(BaseClassifier):
    '''
        spacy 版本
    '''
    # nlp = spacy.load('en')
    # matcher = Matcher(nlp.vocab)
    nlp = None

    def __init__(self):
        '''
            延迟加载, 避免初始化时间过长
        '''
        if not SpacyClassifier.nlp:
            SpacyClassifier.nlp = spacy.load('en')

    def category(self, email):
        '''
            对于一个email 返回所属于分类
        '''
        # 分词, pos, parse, entity(标准部分)
        doc = self.nlp(email)
        if self.is_finance(doc):
            return Category.finance
        return Category.others

    def is_finance(self, doc):
        def find_dollar(doc, ent_id, label, start, end):
            if label in ['subtotal', 'tax']: #如果是这两兄弟, 我们还有查看是不是有后续
                i = 1
                next_token = doc[end+i]
                if next_token.text == ':':
                    i = 2
                    next_token = doc[end+i]
                flag = False
                if next_token.ent_type_ == 'MONEY':
                    flag = True
                if flag:
                    return (ent_id, label, start, end+i)
                else:
                    return None
            else: # 其他的 label 另外处理
                return (ent_id, label, start, end)

        matcher = Matcher(self.nlp.vocab)
        matcher.add_entity('order_payment', acceptor=find_dollar)
        #fixme 当label 我用  str 来传入的时候, 他内部会转成一个 int, 导致我在外面判断的时候不知道值
        #fixme 暂时没有找到办法, 就用 int 传入了
        matcher.add_pattern('order_payment', [{LOWER: 'subtotal'}], label = 1)
        matcher.add_pattern("order_payment", [{LOWER: 'tax'}], label = 2)
        matcher.add_pattern("order_payment", [{LOWER: 'shipping'}], label = 3)

        all_label = [label for ent_id, label, start, end in matcher(doc)]
        # print(all_label)
        if set([1, 2, 3]).issubset(set(all_label)): #表示收集到了这三个 label
            return True
        return False


if __name__ == '__main__':
    '''
        测试一下分类器
    '''
    from resource import load_from_pkl
    sc = SpacyClassifier()
    for id, email in load_from_pkl(start=6643, head=6651):
        # print(email)
        print(sc.category(email['raw']))

# -*- end of file -*-