#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 ashengtx <linls@whu.edu.cn>
# under MIT License

import math


class CilinSimilarity(object):
    """
    基于哈工大同义词词林扩展版计算语义相似度
    """
    def __init__(self):
        """
        'code_word' 以编码为key，单词list为value的dict，一个编码有多个单词
        'word_code' 以单词为key，编码为value的dict，一个单词可能有多个编码
        'vocab' 所有的单词
        'N' N为单词总数，包括重复的词
        """
        self.a = 0.65
        self.b = 0.8
        self.c = 0.9
        self.d = 0.96
        self.e = 0.5
        self.f = 0.1
        self.degree = 180
        self.PI = math.pi
        self.code_word = {}
        self.word_code = {}
        self.vocab = set()
        self.N = 0
        self.read_cilin()

    def read_cilin(self):
        """
        读入同义词词林，编码为key，词群为value，保存在self.code_word
        单词为key，编码为value，保存在self.word_code
        所有单词保存在self.vocab
        """
        with open('../data/cilin.txt', 'r', encoding='gbk') as f:
            for line in f.readlines():
                res = line.split()
                code = res[0]
                words = res[1:]
                self.vocab.update(words)
                self.code_word[code] = words
                self.N += len(words)
                for w in words:
                    if w in self.word_code.keys():
                        self.word_code[w].append(code)
                    else:
                        self.word_code[w] = [code]


    def similarity(self, w1, w2):
        """
        根据下面这篇论文的方法计算的：
        基于同义词词林的词语相似度计算方法，田久乐, 赵 蔚(东北师范大学 计算机科学与信息技术学院, 长春 130117 )

        计算两个单词所有编码组合的相似度，取最大的一个
        """
        # 如果有一个词不在词林中，则相似度为0
        if w1 not in self.vocab or w2 not in self.vocab:
            return 0

        # 获取两个词的编码
        code1 = self.word_code[w1]
        code2 = self.word_code[w2]

        # 最终返回的最大相似度
        sim_max = 0

        # 两个词可能对应多个编码
        for c1 in code1:
            for c2 in code2:
                cur_sim = self.sim_by_code(c1, c2)
                print(c1, c2, '的相似度为：', cur_sim)
                if cur_sim > sim_max:
                    sim_max = cur_sim
        return sim_max

    def sim_by_code(self, c1, c2):
        """
        根据编码计算相似度
        """

        # 先把code的层级信息提取出来
        clayer1 = self.code_layer(c1)
        clayer2 = self.code_layer(c2)

        common_str = self.get_common_str(c1, c2)
        print('common_str: ', common_str)
        length = len(common_str)

        # 如果有一个编码以'@'结尾，那么表示自我封闭，这个编码中只有一个词，直接返回f
        if c1.endswith('@') or c2.endswith('@') or 0 == length:
            return self.f

        cur_sim = 0
        if 7 <= length:
            # 如果前面七个字符相同，则第八个字符也相同，要么同为'='，要么同为'#''
            if c1.endswith('=') and c2.endswith('='):
                cur_sim = 1
            elif c1.endswith('#') and c2.endswith('#'):
                cur_sim = self.e
        else:
            k = self.get_k(clayer1, clayer2)
            n = self.get_n(common_str)
            print('k', k)
            print('n', n)
            if 1 == length:
                cur_sim = self.sim_formula(self.a, n, k)
            elif 2 == length:
                cur_sim = self.sim_formula(self.b, n, k)
            elif 4 == length:
                cur_sim = self.sim_formula(self.c, n, k)
            elif 5 == length:
                cur_sim = self.sim_formula(self.d, n, k)
            
        return cur_sim
    

    def sim_formula(self, coeff, n, k):
        """
        计算相似度的公式，不同的层系数不同
        """
        return coeff * math.cos(n * self.PI / self.degree) * ((n - k + 1) / n)

    def get_common_str(self, c1, c2):
        """
        获取两个字符的公共部分
        """
        res = ''
        for i, j in zip(c1, c2):
            if i == j:
                res += i
            else:
                break
        if 3 == len(res) or 6 == len(res):
            res = res[0:-1]
        return res

    def get_layer(self, common_str):
        """
        根据common_str返回两个编码所在的层数
        如果没有共同的str，则位于第一层，0表示
        第一个字符相同，则位于第二层，1表示
        这里第一层用0表示
        """
        length = len(common_str)
        if 1 == length:
            return 1
        elif 2 == length:
            return 2
        elif 4 == length:
            return 3
        elif 5 == length:
            return 4
        elif 7 == length:
            return 5
        else:
            return 0

    def code_layer(sefl, c):
        """
        将编码按层次结构化
        Aa01A01=
        第三层和第五层是两个数字表示
        第一、二、四层分别是一个字母
        最后一个字符用来去分所有字符相同的情况
        """
        return [c[0], c[1], c[2:4], c[4], c[5:7], c[7]]

    def get_k(self, c1, c2):
        """
        返回两个编码对应分支的距离，相邻距离为1
        """
        if c1[0] != c2[0]:
            return abs(ord(c1[0]) - ord(c2[0]))
        elif c1[1] != c2[1]:
            return abs(ord(c1[1]) - ord(c2[1]))
        elif c1[2] != c2[2]:
            return abs(int(c1[2]) - int(c2[2]))
        elif c1[3] != c2[3]:
            return abs(ord(c1[3]) - ord(c2[3]))
        else:
            return abs(int(c1[4]) - int(c2[4]))

    def get_n(self, common_str):
        """
        计算所在分支层的分支数
        即计算分支的父节点总共有多少个子节点
        两个编码的common_str决定了它们共同处于哪一层
        例如，它们的common_str为前两层，则它们共同处于第三层，则我们统计前两层为common_str的第三层编码个数就好了
        """
        if 0 == len(common_str):
            return 0
        siblings = set()
        layer = self.get_layer(common_str)
        for c in self.code_word.keys():
            if c.startswith(common_str):
                clayer = self.code_layer(c)
                siblings.add(clayer[layer])
        return len(siblings)

    def get_code(self, w):
        """
        返回某个单词的编码
        """
        return self.word_code[w]

    def get_vocab(self):
        """
        返回整个词汇表
        """
        return self.vocab
        
# sim2013 begin =============================
    def sim2013(self, w1, w2):
        """
        根据下面这篇论文的计算方法：
        基于词林的词语相似度的度量，吕立辉，梁维薇， 冉蜀阳，（四川大学计算机科学与技术专业）
        """
        # 如果有一个词不在词林中，则相似度为0
        if w1 not in self.vocab or w2 not in self.vocab:
            return 0

        sigma = 0.3
        codes1 = self.word_code[w1]
        codes2 = self.word_code[w2]
        f1 = self.g1(codes1, codes2)
        f2 = self.g2(codes1, codes2)
        sim = sigma * f1 + (1 - sigma) * f2
        return sim

    def g1(self, codes1, codes2):
        """
        基于词语的路径长度dist(codes1, codes2)计算的相似度
        这里的dist是取两个单词的最短距离
        """
        alpha = 0.47
        return self.epow(-alpha*self.dist(codes1, codes2))

    def g2(self, codes1, codes2):
        """
        考虑密度信息的相似度
        """
        beta = 0.26
        x = beta * self.dense(codes1, codes2)
        return (self.epow(x) - self.epow(-1*x)) / (self.epow(x) + self.epow(-1*x))

    def epow(self, x):
        """
        e^x
        """
        return pow(math.e, x)

    def dist(self, codes1, codes2):
        """
        两个单词的路径距离
        取最短距离
        距离其实就等于5减去公共的层次数再乘以2
        """
        dmin = 0
        for c1 in codes1:
            for c2 in codes2:
                common_str = self.get_common_str(c1, c2)
                layer = self.get_layer(common_str)
                d = 2 * (5 - layer)
                if d > dmin:
                    dmin = d
        return dmin

    def dense(self, codes1, codes2):
        """
        两个单词的密度信息

        这里的密度信息是两个单词所处分支（包括）之间所有分支含有的单词数。
        """
        dns_max = 0
        for c1 in codes1:
            for c2 in codes2:
                #print(self.N)
                #print(self.count_word(c1, c2))
                dns = -1 * math.log(self.count_word(c1, c2)/self.N)# 默认的log以e为底
                if dns > dns_max:
                    dns_max = dns
        return dns_max

    def count_word(self, c1, c2):
        """
        统计两个单词所处分支（包括）之间所有分支含有的单词数。

        首先，找到所有这样的分支，然后将这些分支含有的单词数相加
        """
        codes = self.codes_between(c1, c2)
        cnt = 0
        for code in codes:
            cnt += len(self.code_word[code])
        return cnt

    def codes_between(self, c1, c2):
        """
        获得两个分支之间的所有编码
        """
        codes = set()
        common_str = self.get_common_str(c1, c2)
        all_codes = self.code_word.keys()

        # 如果两个边码相同，则直接返回这个编码
        if len(common_str) == 8:
            codes.add(c1)
            return codes

        for c in all_codes:
            if c.startswith(common_str):
                layer = self.get_layer(common_str)
                clayer = self.code_layer(c)
                if c[layer] <= max(c1[layer], c2[layer]) and c[layer] >= min(c1[layer], c2[layer]):
                    codes.add(c)
        return codes
# sim2013 end =================================

# sim2016 begin ===============================

    def sim2016(self, w1, w2):
        """
        根据以下论文提出的改进方法计算：
        基于知网与词林的词语语义相似度计算，朱新华，马润聪， 孙 柳，陈宏朝（ 广西师范大学 计算机科学与信息工程学院，广西 桂林 ５４１００４）
        """
        # 如果有一个词不在词林中，则相似度为0
        if w1 not in self.vocab or w2 not in self.vocab:
            return 0

        sim_max = 0
        # 获取两个词的编码
        code1 = self.word_code[w1]
        code2 = self.word_code[w2]

        for c1 in code1:
            for c2 in code2:
                cur_sim = self.sim2016_by_code(c1, c2)
                print(c1, c2, cur_sim)
                if cur_sim > sim_max:
                    sim_max = cur_sim
        return sim_max

    def sim2016_by_code(self, c1, c2):
        """
        根据编码计算相似度
        """

        # 先把code的层级信息提取出来
        clayer1 = self.code_layer(c1)
        clayer2 = self.code_layer(c2)

        common_str = self.get_common_str(c1, c2)
        print('common_str: ', common_str)
        length = len(common_str)

        # 如果有一个编码以'@'结尾，那么表示自我封闭，这个编码中只有一个词，直接返回f
        if c1.endswith('@') or c2.endswith('@') or 0 == length:
            return self.f

        cur_sim = 0
        if 7 <= length:
            # 如果前面七个字符相同，则第八个字符也相同，要么同为'='，要么同为'#''
            if c1.endswith('=') and c2.endswith('='):
                cur_sim = 1
            elif c1.endswith('#') and c2.endswith('#'):
                cur_sim = self.e
        else:
            # 从这里开始要改，这之前都一样

            k = self.get_k(clayer1, clayer2)
            n = self.get_n(common_str)
            print('k', k)
            print('n', n)
            d = self.dist2016(common_str)
            print('d', d)
            e = math.sqrt(self.epow(-1 * k / (2*n) ))
            print('e', e)
            cur_sim = (1.05 - 0.05 * d) * e
            
        return cur_sim


    def dist2016(self, common_str):
        """
        计算两个编码的距离
        """
        w1 = 0.5
        w2 = 1
        w3 = 2.5
        w4 = 2.5
        weights = [w1, w2, w3, w4]

        layer = self.get_layer(common_str)

        try :
            if 0 == layer:
                return 18
            else:
                return  2 * sum(weights[0:4-layer+1])
        except Exception as e:
            print('dist2016 errer, 共有的层数不能大于5')


# sim2016 end ====================================

if __name__ == '__main__':
    '''
    有三种计算方法
    cs = CilinSimilarity()
    sim1 = cs.similarity(w1, w2)
    sim2 = cs.sim2013(w1, w2)
    sim3 = cs.sim2016(w1, w2)
    '''

    cs = CilinSimilarity()
    w1 = '抄袭'
    w2 = '克隆'
    code1 = cs.get_code(w1)
    print(w1, '的编码有：', code1)
    code2 = cs.get_code(w2)
    print(w2, '的编码有：', code2)
    sim = cs.similarity(w1, w2)
    print(w1, w2, '最终的相似度为', sim)
