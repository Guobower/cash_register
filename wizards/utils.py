# -*- coding: utf-8 -*-
from random import randint


def random_partition(v, parts):
    res = {}
    for p in parts[1:][::-1]:
        m = v/p
        res[p] = randint(0, m)
        v -= p*res[p]
    res[1] = v
    return res

