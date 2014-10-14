# -*- coding: utf-8 -*-

import random, string
from prioritydict import PriorityDict
from nose.tools import raises
from sys import hexversion
from collections import Counter
from random import randrange as rand

if hexversion < 0x03000000:
    range = xrange

def test_init():
    temp = PriorityDict()
    temp._check()

def test_clear():
    temp = PriorityDict(enumerate(string.lowercase))
    assert len(temp) == 26
    temp.clear()
    assert len(temp) == 0
    temp._check()

def test_clean():
    temp = PriorityDict((val, num) for num, val in enumerate(string.lowercase))
    assert len(temp) == 26
    temp.clean()
    temp._check()
    assert len(temp) == 25
    temp.clean(10)
    temp._check()
    assert len(temp) == 15

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

def test_iloc():
    temp = PriorityDict(enumerate(string.lowercase))
    assert len(temp.iloc) == len(string.lowercase)

def test_iloc_getitem():
    temp = PriorityDict(enumerate(string.lowercase))
    for pos, letter in enumerate(string.lowercase):
        assert temp[temp.iloc[pos]] == letter
    temp._check()

def test_iloc_getitem_slice():
    temp = PriorityDict(enumerate(string.lowercase))
    that = list(enumerate(string.lowercase))
    assert temp.iloc[5:20:3] == list(len(string.lowercase))[5:20:3]

def test_iloc_delitem():
    temp = PriorityDict(enumerate(string.lowercase))
    that = list(enumerate(string.lowercase))

    while len(temp) > 0:
        pos = rand(len(temp))
        del that[pos]
        del temp.iloc[pos]
        assert temp.items() == that
        temp._check()

def test_iloc_delitem_slice():
    temp = PriorityDict(enumerate(string.lowercase))
    that = list(enumerate(string.lowercase))
    del temp.iloc[5:20:3]
    del that[5:20:3]
    assert temp.items() == that
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
    assert len(that) == 4
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

def test_count():
    seq = list((val, pos) for pos, val in enumerate(string.lowercase))
    pd = PriorityDict.count(val for val, pos in seq for num in range(pos))
    c = Counter(val for val, pos in seq for num in range(pos))
    assert pd == c

def test_update_small():
    temp = PriorityDict((val, pos) for pos, val in enumerate(string.lowercase))
    temp.update((val, -pos) for pos, val in enumerate(string.lowercase[10:14]))
    for pos, val in enumerate(string.lowercase[10:14]):
        assert temp[val] == -pos

def test_update_big():
    temp = PriorityDict((val, pos) for pos, val in enumerate(string.lowercase))
    temp.update((val, -pos) for pos, val in enumerate(string.lowercase[5:25]))
    for pos, val in enumerate(string.lowercase[5:25]):
        assert temp[val] == -pos

def test_index():
    temp = PriorityDict((val, pos) for pos, val in enumerate(string.lowercase))
    for key in string.lowercase:
        pos = temp.index(key)
        assert temp.iloc[pos] == key

@raises(KeyError)
def test_index_keyerror():
    temp = PriorityDict((val, pos) for pos, val in enumerate(string.lowercase))
    temp.index('aa')

def test_bisect_left():
    temp = PriorityDict((val, (val / 10) * 10) for val in range(100))
    for val in range(100):
        assert temp.bisect_left(val) == ((val + 9) / 10) * 10

def test_bisect():
    temp = PriorityDict((val, (val / 10) * 10) for val in range(100))
    for val in range(100):
        assert temp.bisect_left(val) == ((val + 9) / 10) * 10

def test_bisect_right():
    temp = PriorityDict((val, (val / 10) * 10) for val in range(100))
    for val in range(100):
        assert temp.bisect_right(val) == ((val + 10) / 10) * 10

def test_iadd_small():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(10))
    temp += that
    assert all(temp[val] == 2 * val for val in range(10))
    assert all(temp[val] == val for val in range(10, 100))
    temp._check()

def test_iadd_big():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(100))
    temp += that
    assert all(temp[val] == 2 * val for val in range(100))
    temp._check()

def test_isub_small():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(10))
    temp -= that
    assert all(temp[val] == 0 for val in range(10))
    assert all(temp[val] == val for val in range(10, 100))
    temp._check()

def test_isub_big():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(100))
    temp -= that
    assert all(temp[val] == 0 for val in range(100))
    temp._check()

def test_ior_small():
    temp_vals = list((val, rand(100)) for val in range(100))
    that_vals = list((val, rand(100)) for val in range(10))
    temp = PriorityDict(temp_vals)
    that = PriorityDict(that_vals)
    temp |= that
    assert all(temp[pos] == max(temp_vals[pos][1], that_vals[pos][1])
               for pos in range(10))
    assert all(temp[pos] == temp_vals[pos][1]
               for pos in range(10, 100))
    temp._check()

def test_ior_big():
    temp_vals = list((val, rand(100)) for val in range(100))
    that_vals = list((val, rand(100)) for val in range(100))
    temp = PriorityDict(temp_vals)
    that = PriorityDict(that_vals)
    temp |= that
    assert all(temp[pos] == max(temp_vals[pos][1], that_vals[pos][1])
               for pos in range(100))
    temp._check()

def test_iand_small():
    temp_vals = list((val, rand(100)) for val in range(100))
    that_vals = list((val, rand(100)) for val in range(10))
    temp = PriorityDict(temp_vals)
    that = PriorityDict(that_vals)
    temp &= that
    assert all(temp[pos] == min(temp_vals[pos][1], that_vals[pos][1])
               for pos in range(10))
    assert all(temp[pos] == temp_vals[pos][1]
               for pos in range(10, 100))
    temp._check()

def test_iand_big():
    temp_vals = list((val, rand(100)) for val in range(100))
    that_vals = list((val, rand(100)) for val in range(100))
    temp = PriorityDict(temp_vals)
    that = PriorityDict(that_vals)
    temp &= that
    assert all(temp[pos] == min(temp_vals[pos][1], that_vals[pos][1])
               for pos in range(100))
    temp._check()

def test_add():
    temp_vals = list((val, rand(100)) for val in range(100))
    that_vals = list((val, rand(100)) for val in range(50))
    temp = PriorityDict(temp_vals)
    that = PriorityDict(that_vals)
    other = temp + that
    other._check()
    assert len(other) == 100
    assert all(other[pos] == (temp_vals[pos][1] + that_vals[pos][1])
               for pos in range(50))
    assert all(other[pos] == temp_vals[pos][1] for pos in range(50, 100))

def test_sub():
    temp_vals = list((val, rand(100)) for val in range(25, 75))
    that_vals = list((val, rand(100)) for val in range(100))
    temp = PriorityDict(temp_vals)
    that = PriorityDict(that_vals)
    other = temp - that
    other._check()
    assert len(other) == 50
    assert all(other[pos] == (temp_vals[pos - 25][1] - that_vals[pos][1])
               for pos in range(25, 75))

def test_or():
    temp_vals = list((val, rand(100)) for val in range(100))
    that_vals = list((val, rand(100)) for val in range(50))
    temp = PriorityDict(temp_vals)
    that = PriorityDict(that_vals)
    other = temp | that
    other._check()
    assert len(other) == 100
    assert all(other[pos] == max(temp_vals[pos][1], that_vals[pos][1])
               for pos in range(50))
    assert all(other[pos] == temp_vals[pos][1] for pos in range(50, 100))

def test_and():
    temp_vals = list((val, rand(100)) for val in range(25, 75))
    that_vals = list((val, rand(100)) for val in range(100))
    temp = PriorityDict(temp_vals)
    that = PriorityDict(that_vals)
    other = temp & that
    other._check()
    assert len(other) == 50
    assert all(other[pos] == min(temp_vals[pos - 25][1], that_vals[pos][1])
               for pos in range(25, 75))

def test_eq():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(100))
    assert temp == that
    that[50] = -50
    assert not (temp == that)

def test_ne():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(100))
    assert not (temp != that)
    that[50] = -50
    assert temp != that

def test_lt():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(100))
    temp[50] = -50
    assert temp < that
    del temp[0]
    assert temp < that
    del that[1]
    assert not (temp < that)

def test_le():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(100))
    assert temp <= that
    temp[50] = -50
    assert temp <= that
    del temp[0]
    assert temp <= that
    del that[1]
    assert not (temp <= that)

def test_gt():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(100))
    that[50] = -50
    assert temp > that
    del that[0]
    assert temp > that
    del temp[1]
    assert not (temp > that)

def test_ge():
    temp = PriorityDict((val, val) for val in range(100))
    that = PriorityDict((val, val) for val in range(100))
    assert temp >= that
    that[50] = -50
    assert temp >= that
    del that[0]
    assert temp >= that
    del temp[1]
    assert not (temp >= that)

def test_isdisjoint():
    temp = PriorityDict((val, val) for val in range(50))
    that = PriorityDict((val, val) for val in range(50, 100))
    assert temp.isdisjoint(that)

def test_items():
    pass

def test_keys():
    pass

def test_values():
    pass

def test_repr():
    pass
