# -*- coding: utf-8 -*-
# !/usr/bin/env python

import pickle
from pprint import pprint
from collections import defaultdict

class GoldStandard(object):
    '''
        读取一个 email 输入, 通过人工给出分类的答案, 本地存储
    '''
    tag_option = ['conversation', 'order-shipping', 'order-acknowledgement', 'others']

    def __init__(self, input_stream=None, out_name='gold', data=None):
        '''
        :param input_stream: 可以遍历的一个迭代器, 每个 item 包含了所需的数据
        :param out_name: 本地存储的文件名
        :param data: 用户数据
        :param tag: 标注的数据
        '''
        self.stream = input_stream
        self.out_name = out_name
        self.data = data if data else [] #测试数据

    def save(self):
        '''
            保存到本地文件, 把这次人工标注结果记录下来
        '''
        with open(self.out_name, 'rb') as f:
            pickle.dump(dict(
                data=self.data,
                out_name=self.out_name
            ), f)

    @classmethod
    def load_from_file(cls, pkl_name):
        '''
            从本地文件中生成一个 GoldStandard
            注意这里的 classmethod 函数和 Spacy->Matcher->load函数的用法
        '''
        with open(pkl_name, 'rb') as f:
            obj = pickle.load(f)
            return GoldStandard(out_name=obj['out_name'], data=obj['data'])

    def tag(self):
        '''
            遍历数据, 人工标记分类, 对于 email, 逐封打印在控制台, 输入所属于的分类
            但我发现这样的确实好几十封才能找到所需的, 所以换一个另一个 tag 的方式
        '''
        if not self.stream:
            raise NotImplementedError()

        goon = True
        for row in self.stream:
            pprint(row)
            while True:
                tag = input('Input the correct Category:  ')
                if tag == 'quit':
                    goon = False
                    break
                real_tag = [i for i in self.tag_option if tag in i]
                if real_tag and len(real_tag) == 1: # 只有一个命中
                    real_tag = real_tag[0] # 只取一个值
                    break
                print('Incorrect Category!')

            if not goon:
                break
            self.data.append((row, real_tag))


class GoldEmail(object):
    '''
        用直接指定的方式, 告诉哪些 id 是属于哪个分类的
    '''
    def __init__(self, input_stream, tag_map):
        '''
        :param input_stream: 同样传入的数据
        :param tag_map: {id: category}
        '''
        # 从 input_stream 中找到我所需要的 id
        all_data = dict(input_stream)
        self.data = [(all_data[id], category) for id, category in tag_map.items()]
        del all_data # 节省空间

    def verify(self, classifier):
        '''
            验证这个分类器的准确率和召回率
        '''
        real_tag = defaultdict(set)
        cal_tag = defaultdict(set)
        for data, category in self.data:
            cal_cate = classifier.category(data['raw'])
            real_tag[category].add(data['id'])
            cal_tag[cal_cate].add(data['id'])

        # 以下计算都是针对某个类别的
        # 计算准确率: P=tp/(tp+fp)
        precision = {c:len(cal_tag[i].intersection(real_tag[i]))/len(cal_tag) for c in cal_tag}

        # 计算召回率: R=tp/(tp+fn)
        recall = {c:len(cal_tag[i].intersection(real_tag[i]))/len(real_tag) for c in cal_tag}

        # 计算 f1值: 2/f1 = 1/P + 1/R
        f1 = {2*precision[c]*recall[c]/(precision[c]+recall[c]) for c in cal_tag}

        pprint(f1)






# -*- end of file -*-