# -*- coding: utf-8 -*-
#
# PriorityDict implementation.

from sortedcontainers import SortedList

from collections import MutableMapping
from collections import KeysView as AbstractKeysView
from collections import ValuesView as AbstractValuesView
from collections import ItemsView as AbstractItemsView

from itertools import chain, repeat

class _IlocWrapper:
    def __init__(self, _dict):
        self._dict = _dict

    def __len__(self):
        return len(self._dict)

    def __getitem__(self, index):
        """
        Very efficiently return the key at index *index* in iteration. Supports
        negative indices and slice notation. Raises IndexError on invalid
        *index*.
        """
        return self._dict._list[index]

    def __delitem__(self, index):
        """
        Remove the ``sdict[sdict.iloc[index]]`` from *sdict*. Supports negative
        indices and slice notation. Raises IndexError on invalid *index*.
        """
        if isinstance(index, slice):
            keys = self._dict._list[index]
            del self._dict._list[index]
            for key in keys:
                del self._dict._dict[key]
        else:
            key = self._dict._list[index]
            del self._dict._list[index]
            del self._dict._dict[key]

class PriorityDict(MutableMapping):
    def __init__(self, values=None):
        self._dict = dict()
        self._list = SortedList()
        self.iloc = _IlocWrapper(self)

        if values is not None:
            self.update(values)

    def clear(self):
        """Remove all elements from the dictionary."""
        self._dict.clear()
        self._list.clear()

    def __contains__(self, key):
        """Return True if and only if *key* is in the dictionary."""
        return key in self._dict

    def __delitem__(self, key):
        """
        Remove ``d[key]`` from *d*.  Raises a KeyError if *key* is not in the
        dictionary.
        """
        value = self._dict[key]
        self._list.remove((value, key))
        del self._dict[key]

    def __getitem__(self, key):
        """
        Return the priority in *d* of *key*.  Raises a KeyError if *key* is not
        in the dictionary.
        """
        return self._dict[key]

    def __eq__(self, that):
        raise NotImplementedError
    def __ne__(self, that):
        raise NotImplementedError

    def __iter__(self):
        """
        Create an iterator over the keys of the dictionary ordered by the value
        sort order.
        """
        return iter(tup[1] for tup in self._list)

    def __reversed__(self):
        """
        Create an iterator over the keys of the dictionary ordered by the
        reversed value sort order.
        """
        return iter(tup[1] for tup in reversed(self._list))

    def __len__(self):
        """Return the number of (key, value) pairs in the dictionary."""
        return len(self._dict)

    def __setitem__(self, key, priority):
        if key in self._dict:
            value = self._dict[key]
            self._list.remove((value, key))
        self._list.add((priority, key))
        self._dict[key] = priority

    def copy(self):
        """Create a shallow copy of the dictionary."""
        that = PriorityDict()
        that._dict = self._dict
        that._list = self._list
        that.iloc = self.iloc
        return that

    @classmethod
    def fromkeys(cls, iterable, value=0):
        """
        Create a new dictionary with keys from *iterable* and values set to
        *value*. The default *value* is 0.
        """
        return PriorityDict((key, value) for key in iterable)

    def get(self, key, default=None):
        """
        Return the value for *key* if *key* is in the dictionary, else
        *default*.  If *default* is not given, it defaults to ``None``,
        so that this method never raises a KeyError.
        """
        return self._dict.get(key, default)

    def has_key(self, key):
        """Return True if and only in *key* is in the dictionary."""
        return key in self._dict

    def items(self):
        # TODO: Pickup at line 179 in sorteddict.py
        raise NotImplementedError

    @classmethod
    def fromcounter(cls, counter):
        return PriorityDict(counter)

    def elements(self):
        """
        Return an iterator over elements repeating each as many times as its
        count. Elements are returned in value sort-order. If an element’s count
        is less than one, elements() will ignore it.
        """
        values = (repeat(tup[1], tup[0]) for tup in self._list)
        return chain.from_iterable(values)

    def most_common(self, count=None):
        """
        Return a list of the `count` highest priority elements with their
        priority. If `count` is not specified, `most_common` returns *all*
        elements in the dict. Elements with equal counts are ordered by key.
        """
        end = len(self._dict)

        if count is None:
            count = end

        start = end - count

        return [(tup[1], tup[0]) for tup in self._list[start:end:-1]]

    def subtract(self, elements):
        """
        Elements are subtracted from an iterable or from another mapping (or
        counter). Like dict.update() but subtracts counts instead of replacing
        them. Both inputs and outputs may be zero or negative.
        """
        raise NotImplementedError

    def update(self, iterable):
        """
        Elements are counted from an iterable or added-in from another mapping
        (or counter). Like dict.update() but adds counts instead of replacing
        them. Also, the iterable is expected to be a sequence of elements, not a
        sequence of (key, value) pairs.
        """
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def popleft(self):
        raise NotImplementedError
