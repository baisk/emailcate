# -*- coding: utf-8 -*-
# !/usr/bin/env python

from resource import load_from_pkl

from goldtest import GoldStandard

def test_load():
    for i in load_from_pkl(head=10):
        print(i)
    pass

def test_gold():
    g = GoldStandard(load_from_pkl(head=10), out_name='test')
    g.tag()


if __name__ == '__main__':
    # test_load()
    test_gold()
# -*- end of file -*-