# -*- coding: utf-8 -*-
from random import randint


def random_partition(n, parts):
    """
    :param n: int
    :param parts: list
    :return: dict

    This algorithm takes an integer, n, and a list, parts, of integers and
    returns a dictionary of key, values (k,v) correspond to an integer
    partition of n with v copies of k.

    Example: if (n, parts) = (5, [1,2,3]) a possible output could be any of
    {1: 0, 2: 1, 3: 1},
    {1: 2, 2: 0, 3: 1},
    {1: 1, 2: 2, 3: 0},
    {1: 3, 2: 1, 3: 0},
    {1: 5, 2: 0, 3: 0}

    with (I think) equal probability.
    """
    res = {}
    for p in reversed(parts[1:]):
        res[p] = randint(0, n // p)
        n -= p * res[p]

    res[1] = n
    return res
