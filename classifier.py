# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
    分类器, 对于每一个email, 单独调用类去判别, 输出所属的分类
'''

import spacy
from spacy.matcher import Matcher
from enum import IntEnum

class Category(IntEnum):
    conversation = 1
    order_shipping = 2
    order_acknowledgement = 3
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
    nlp = spacy.load('en')
    matcher = Matcher(nlp.vocab)

    def category(self, email):
        '''
            对于一个email 返回所属于分类
        '''
        pass


# -*- end of file -*-