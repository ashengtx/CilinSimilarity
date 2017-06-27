# CilinSimilarity
Word similarity computation based on Tongyici Cilin

这是一个基于哈工大同义词词林扩展版的单词相似度计算方法的python实现，参考了三篇paper，实现了三种相似度的计算方法。

三篇paper分别为：

- 2010 田久乐等，吉林大学学报（信息科学版），[基于同义词词林的词语相似度计算方法](http://www.cnki.net/KCMS/detail/detail.aspx?QueryID=2&CurRec=1&recid=&filename=CCYD201006010&dbname=CJFD2010&dbcode=CJFQ&pr=&urlid=&yx=&v=MjUwNjl1Wm5GeTNuVkwzSkppN1Nhckc0SDlITXFZOUVaSVI4ZVgxTHV4WVM3RGgxVDNxVHJXTTFGckNVUkx5ZVo=)
- 2013 吕立辉等，现代计算机（专业版），[基于词林的词语相似度的度量](http://www.cnki.net/KCMS/detail/detail.aspx?QueryID=2&CurRec=9&recid=&filename=XDJS201301002&dbname=CJFD2013&dbcode=CJFQ&pr=&urlid=&yx=&v=Mjc5NDFyQ1VSTHllWnVabkZ5M25WTHZMUFNuQmZiRzRIOUxNcm85RlpvUjhlWDFMdXhZUzdEaDFUM3FUcldNMUY=)
- 2016 朱新华等，中文信息学报，[基于知网与词林的词语语义相似度计算](http://www.cnki.net/KCMS/detail/detail.aspx?QueryID=2&CurRec=14&recid=&filename=MESS201604004&dbname=CJFDTEMP&dbcode=CJFQ&pr=&urlid=&yx=&v=MDMwODR1eFlTN0RoMVQzcVRyV00xRnJDVVJMeWVadVpuRnkzblZidklLQ2pZZmJHNEg5Zk1xNDlGWUlSOGVYMUw=)

### Usage

- python3
- 直接clone到本地即可使用

示例如下
```python
cs = CilinSimilarity()
w1 = '抄袭'
w2 = '克隆'
code1 = cs.get_code(w1)
print(w1, '的编码有：', code1)
code2 = cs.get_code(w2)
print(w2, '的编码有：', code2)
sim = cs.similarity(w1, w2)
print(w1, w2, '最终的相似度为', sim)
```
输出结果如下
```python
抄袭 的编码有： ['Hb08B04=', 'Hn10C01=']
克隆 的编码有： ['Hd04A03=']
common_str:  H
k 2
n 14
Hb08B04= Hd04A03= 的相似度为： 0.585642777645155
common_str:  H
k 10
n 14
Hn10C01= Hd04A03= 的相似度为： 0.22524722217121346
抄袭 克隆 最终的相似度为 0.585642777645155
```
[2013]和[2016]两篇的计算方法，分别调用```cs.sim2013(w1, w2)```和```cs.sim2016(w1, w2)```即可。

如有错误，请指正，lls9107@qq.com
