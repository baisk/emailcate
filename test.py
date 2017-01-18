# -*- coding: utf-8 -*-
# !/usr/bin/env python

from resource import load_from_pkl

from goldtest import GoldStandard, GoldEmail
from classifier import Category, ReClassifier

def test_load():
    for i in load_from_pkl(head=10):
        print(i)
    pass

def test_gold():
    g = GoldStandard(load_from_pkl(head=10), out_name='test')
    g.tag()

def test_gold_email():
    # 假数据
    tag_map = {
        'bqtadyqz1efpeuwbfoqfmkqi3': Category.conversation,
        'bmkxm638ky7gs6xb2h8ydjq5d': Category.order_acknowledgement,
    }

    g = GoldEmail(input_stream=load_from_pkl(),tag_map=tag_map)
    g.verify(ReClassifier())

if __name__ == '__main__':
    # test_load()
    # test_gold()
    # test_gold_email()
    pass
# -*- end of file -*-