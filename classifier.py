# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
    分类器, 对于每一个email, 单独调用类去判别, 输出所属的分类
'''

import spacy
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
    pass


class ReClassifier(BaseClassifier):
    '''
        正则版本
    '''
    pass


class SpacyClassifier(BaseClassifier):
    '''
        spacy 版本
    '''
    nlp = spacy.load('en')

    pass


# -*- end of file -*-