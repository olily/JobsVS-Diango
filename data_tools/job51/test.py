# -*- coding: utf-8 -*-
__author__ = 'olily'


import math
import jieba
from sklearn.metrics.pairwise import cosine_similarity

a = [[5,0.1,0.2,0.2,0.4,0.5],[1,0.1,0.2,0.2,0.4,0.5]]
b = [[3,0.5,0.2,0.2,0.4,0.5],[3,0.1,0.2,0.2,0.4,0.5]]
t = cosine_similarity(a)
t2 = cosine_similarity(b)

print(type(t))
print(t[0][1],t2[0][1])