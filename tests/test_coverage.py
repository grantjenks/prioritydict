# -*- coding: utf-8 -*-

import random, string
from prioritydict import PriorityDict
from nose.tools import raises
from sys import hexversion

def get_keysview(dic):
    if hexversion < 0x03000000:
        return dic.viewkeys()
    else:
        return dic.keys()

def get_valuesview(dic):
    if hexversion < 0x03000000:
        return dic.viewvalues()
    else:
        return dic.values()

def get_itemsview(dic):
    if hexversion < 0x03000000:
        return dic.viewitems()
    else:
        return dic.items()

def test_init():
    temp = PriorityDict()
    temp._check()
