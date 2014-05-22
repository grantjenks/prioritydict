# -*- coding: utf-8 -*-

import random, string
from prioritydict import PriorityDict
from nose.tools import raises
from sys import hexversion

if hexversion < 0x03000000:
    range = xrange

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

def test_clear():
    temp = PriorityDict(enumerate(string.lowercase))
    assert len(temp) == 26
    temp.clear()
    assert len(temp) == 0
    temp._check()

def test_contains():
    temp = PriorityDict(enumerate(string.lowercase))
    assert all(pos in temp for pos in range(len(string.lowercase)))
    assert 26 not in temp
    assert not (-1 in temp)
    temp._check()

def test_delitem():
    temp = PriorityDict(enumerate(string.lowercase))
    del temp[13]
    assert len(temp) == 25
    temp._check()

def test_getitem():
    temp = PriorityDict(enumerate(string.lowercase))
    for pos, letter in enumerate(string.lowercase):
        assert temp[pos] == letter
    temp._check()

def test_iter():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    assert list(iter(temp)) == list(string.lowercase)
    temp._check()

def test_reversed():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    assert list(reversed(temp)) == list(reversed(string.lowercase))
    temp._check()

def test_len():
    temp = PriorityDict()
    assert len(temp) == 0
    val = dict((letter, pos) for pos, letter in enumerate(string.lowercase))
    temp.update(val)
    assert len(temp) == 26
    temp._check()

def test_setitem():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    for pos, key in enumerate(reversed(string.lowercase)):
        temp[key] = pos
    assert list(reversed(string.lowercase)) == list(temp)
    temp._check()

def test_copy():
    this = PriorityDict({'a': 0, 'b': 1, 'c': 2, 'd': 3})
    that = this.copy()
    del this['d']
    assert len(that) == 3
    this._check()
    that._check()

def test_fromkeys():
    temp = PriorityDict.fromkeys(string.lowercase, 100)
    temp['m'] = 0
    assert temp.iloc[0] == 'm'
    temp._check()

def test_get():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    assert temp.get('a') == 0
    assert temp.get('y') == 24
    assert temp.get('blah') == None
    temp._check()

def test_has_key():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    assert temp.has_key('r')
    temp._check()

def test_pop():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    assert temp.pop('c') == 2
    temp._check()
    assert temp.pop('blah', -1) == -1
    temp._check()

@raises(KeyError)
def test_pop_error():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    temp.pop('blah')

def test_popitem():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    assert (temp.popitem() == ('z', 25))
    assert (temp.popitem() == ('y', 24))
    assert (temp.popitem(0) == ('a', 0))
    temp._check()

def test_setdefault():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    assert temp.setdefault('d', -1) == 3
    assert temp.setdefault('blah', 10) == 10
    temp._check()
    assert len(temp) == 27
    assert temp['k'] == 10
    temp._check()

def test_elements():
    temp = PriorityDict({'a': 3, 'b': 2, 'c': 1})
    assert ['c', 'b', 'b', 'a', 'a', 'a'] == list(temp.elements())

def test_most_common():
    temp = PriorityDict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
    assert temp.most_common() == [('d', 4), ('c', 3), ('b', 2), ('a', 1)]
    assert temp.most_common(2) == [('d', 4), ('c', 3)]
    temp._check()

def test_subtract():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    temp.subtract(list(string.lowercase))
    for pos, key in enumerate(string.lowercase):
        assert temp[key] == (pos - 1)
    temp._check()

def test_tally():
    temp = PriorityDict((val, key) for key, val in enumerate(string.lowercase))
    temp.tally(list(string.lowercase))
    for pos, key in enumerate(string.lowercase):
        assert temp[key] == (pos + 1)
    temp._check()

def test_lt():
    assert not (PriorityDict({'a': 1}) < PriorityDict({'b': 2, 'c': 3}))

def test_items():
    pass

def test_keys():
    pass

def test_values():
    pass
