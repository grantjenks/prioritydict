# -*- coding: utf-8 -*-
#
# PriorityDict implementation.

from sortedcontainers import SortedList

from collections import MutableMapping
from collections import KeysView as AbstractKeysView
from collections import ValuesView as AbstractValuesView
from collections import ItemsView as AbstractItemsView

from itertools import chain, repeat

_NotGiven = object()

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
    def __init__(self, *args, **kwargs):
        self._dict = Counter()
        self._list = SortedList()
        self.iloc = _IlocWrapper(self)
        self.update(*args, **kwargs)

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
        Return the priority of *key* in *d*.  Raises a KeyError if *key* is not
        in the dictionary.
        """
        return self._dict[key]

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

    def __setitem__(self, key, value):
        if key in self._dict:
            value = self._dict[key]
            self._list.remove((value, key))
        self._list.add((value, key))
        self._dict[key] = value

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
        raise NotImplementedError
    def iteritems(self):
        raise NotImplementedError
    def viewitems(self):
        raise NotImplementedError
    def keys(self):
        raise NotImplementedError
    def iterkeys(self):
        raise NotImplementedError
    def viewkeys(self):
        raise NotImplementedError
    def values(self):
        raise NotImplementedError
    def itervalues(self):
        raise NotImplementedError
    def viewvalues(self):
        raise NotImplementedError
    
    def pop(self, key, default=_NotGiven):
        """
        If *key* is in the dictionary, remove it and return its value,
        else return *default*. If *default* is not given and *key* is not in
        the dictionary, a KeyError is raised.
        """
        if key in self._dict:
            value = self._dict[key]
            self._list.remove((value, key))
            return self._dict.pop(key)
        else:
            if default == _NotGiven:
                raise KeyError
            else:
                return default

    def popitem(self, index=-1):
        """
        Remove and return item at *index* (default: -1). Raises IndexError if
        dict is empty or index is out of range. Negative indices are supported
        as for slice indices.
        """
        value, key = self._list.pop(index)
        del self._dict[key]
        return key, value

    def setdefault(self, key, default=0):
        """
        If *key* is in the dictionary, return its value.  If not, insert *key*
        with a value of *default* and return *default*.  *default* defaults to
        ``0``.
        """
        if key in self._dict:
            return self._dict[key]
        else:
            self._dict[key] = default
            self._list.add((default, key))
            return default

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
        self -= Counter(elements)

    def update(self, *args, **kwargs):
        """
        Elements are counted from an iterable or added-in from another mapping
        (or counter). Like dict.update() but adds counts instead of replacing
        them. Also, the iterable is expected to be a sequence of elements, not a
        sequence of (key, value) pairs.
        """
        self += Counter(*args, **kwargs)

    def index(self, key):
        """
        Return the smallest *k* such that `d.iloc[k] == key`.  Raises KeyError
        if *key* is not present.
        """
        value = self._dict[key]
        return self._list.index((value, key))

    def index_value(self, value):
        """
        Return the smallest *k* such that `d[d.iloc[k]] == value`. Raises
        ValueError if *value* is not present.
        """
        pos = self._list.bisect_left((value,))
        if pos == len(self._dict) or self._list[pos][0] != value:
            raise ValueError
        else:
            return pos

    def bisect_left(self, priority):
        return self._list.bisect_left((priority,))

    def bisect(self, priority):
        return self._list.bisect((priority,))

    def bisect_right(self, priority):
        return self._list.bisect_right((priority,))

    def __add__(self, that):
        result = PriorityDict(self)
        result += that
        return result

    def __iadd__(self, that):
        raise NotImplementedError

    def __sub__(self, that):
        result = PriorityDict(self)
        result -= that
        return result

    def __isub__(self, that):
        raise NotImplementedError

    def __and__(self, that):
        result = PriorityDict(self)
        result &= that
        return result

    def __iand__(self, that):
        raise NotImplementedError

    def __or__(self, that):
        result = PriorityDict(self)
        result |= that
        return result

    def __ior__(self, that):
        raise NotImplementedError

    def __eq__(self, that):
        """Compare two mappings for equality."""
        if isinstance(that, PriorityDict):
            that = that._dict
        return self._dict == that

    def __ne__(self, that):
        """Compare two mappings for inequality."""
        if isinstance(that, PriorityDict):
            that = that._dict
        return self._dict != that

    def __lt__(self, that):
        """Compare two mappings for less than."""
        if isinstance(that, PriorityDict):
            that = that._dict
        return self._dict < that

    def __le__(self, that):
        """Compare two mappings for less than equal."""
        if isinstance(that, PriorityDict):
            that = that._dict
        return self._dict <= that

    def __gt__(self, that):
        """Compare two mappings for greater than."""
        if isinstance(that, PriorityDict):
            that = that._dict
        return self._dict > that

    def __ge__(self, that):
        """Compare two mappings for greater than equal."""
        if isinstance(that, PriorityDict):
            that = that._dict
        return self._dict >= that

    def __repr__(self):
        """Return string representation of PriorityDict."""
        return 'PriorityDict({0})'.format(repr(dict(self)))

    def _check(self):
        self._list._check()
        assert len(self._dict) == len(self._list)
        assert all(key in self._dict and self._dict[key] == value
                   for value, key in self._list)
