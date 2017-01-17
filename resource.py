# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
    email的输入来源, 可以从本地读取, 也可以从网上读取
'''
import pickle
import itertools

def load_from_pkl(pkl_name='email_sample_joey.pkl', head=None):
    '''
        从 pickle 文件中读取 email, 如果指定 head, 则返回前 head 条, head 为int

        这里的 pkl 文件格式:
            [
                {id: {
                        'account_id':
                        'body':
                        'clean_body':
                        'from':
                        'id':
                        ....
                    }
                }
                ...
            ]
    '''
    #fixme 如果文件太大, 以下代码就有问题, 相当于一次性加载到内存中
    #fixme 可以通过批量读取加载的方式
    with open(pkl_name, 'rb') as f:
        emails = pickle.load(f)
        for email_id, email in itertools.islice(emails.items(), head):
            yield dict(
                id = email['id'],
                raw = email['clean_body']
            )

# load_from_pkl = _load_from_pkl

# -*- end of file -*-