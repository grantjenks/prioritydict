# -*- coding: utf-8 -*-

"""
PriorityDict Implementation
===========================

PriorityDict is an Apache2 licensed implementation of a dictionary which
maintains key-value pairs in value sort order.
"""

from sortedcontainers import SortedList

from collections import Counter, MutableMapping, Set, Sequence
from collections import KeysView as AbstractKeysView
from collections import ValuesView as AbstractValuesView
from collections import ItemsView as AbstractItemsView

from functools import wraps
from itertools import chain, repeat
from sys import hexversion

_NotGiven = object()

class _Biggest:
    """An object that is greater than all others."""
    def __gt__(self, that):
        return True
    def __ge__(self, that):
        return True
    def __lt__(self, that):
        return False
    def __le__(self, that):
        return False
    def __eq__(self, that):
        return False
    def __ne__(self, that):
        return True

_Biggest = _Biggest()

def not26(func):
    """Function decorator for methods not implemented in Python 2.6."""

    @wraps(func)
    def errfunc(*args, **kwargs):
        raise NotImplementedError

    if hexversion < 0x02070000:
        return errfunc
    else:
        return func

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
        if isinstance(index, slice):
            return [tup[1] for tup in self._dict._list[index]]
        else:
            return self._dict._list[index][1]

    def __delitem__(self, index):
        """
        Remove the ``sdict[sdict.iloc[index]]`` from *sdict*. Supports negative
        indices and slice notation. Raises IndexError on invalid *index*.
        """
        if isinstance(index, slice):
            keys = [tup[1] for tup in self._dict._list[index]]
            del self._dict._list[index]
            for key in keys:
                del self._dict._dict[key]
        else:
            key = self._dict._list[index][1]
            del self._dict._list[index]
            del self._dict._dict[key]

class PriorityDict(MutableMapping):
    """
    A PriorityDict provides the same methods as a dict. Additionally, a
    PriorityDict efficiently maintains its keys in value sorted order.
    Consequently, the keys method will return the keys in value sorted order,
    the popitem method will remove the item with the highest value, etc.
    """
    def __init__(self, *args, **kwargs):
        """
        A PriorityDict provides the same methods as a dict. Additionally, a
        PriorityDict efficiently maintains its keys in value sorted order.
        Consequently, the keys method will return the keys in value sorted
        order, the popitem method will remove the item with the highest value,
        etc.

        An optional *iterable* provides an initial series of items to
        populate the PriorityDict. Like collections.Counter, items are
        counted from iterable.

        If keyword arguments are given, the keywords themselves with their
        associated values are added as items to the dictionary. If a key is
        specified both in the positional argument and as a keyword argument,
        the value associated with the keyword is retained in the dictionary.
        For example, these all return a dictionary equal to ``{"one": 2,
        "two": 3}``:

        * ``PriorityDict(one=2, two=3)``
        * ``PriorityDict({'one': 2, 'two': 3})``
        * ``PriorityDict(['one', 'two', 'one', 'two', 'two')``

        The first example only works for keys that are valid Python
        identifiers; the others work with any valid keys.
        """
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
        """Set `d[key]` to *value*."""
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
        """
        In Python 2, returns a list of the dictionary's items (``(key, value)``
        pairs).

        In Python 3, returns a new ItemsView of the dictionary's items.  In
        addition to the methods provided by the built-in `view` the ItemsView is
        indexable (e.g., ``d.items()[5]``).
        """
        if hexversion < 0x03000000:
            return list((key, value) for value, key in self._list)
        else:
            return ItemsView(self)

    def iteritems(self):
        """Return an iterable over the items (``(key, value)`` pairs)."""
        return iter((key, value) for value, key in self._list)

    @not26
    def viewitems(self):
        """
        In Python 2.7 and later, return a new `ItemsView` of the dictionary's
        items.

        In Python 2.6, raise a NotImplementedError.
        """
        return ItemsView(self)

    def keys(self):
        """
        In Python 2, return a list of the dictionary's keys.

        In Python 3, return a new KeysView of the dictionary's keys.  In
        addition to the methods provided by the built-in `view` the KeysView is
        indexable (e.g., ``d.keys()[5]``).
        """
        if hexversion < 0x03000000:
            return list(key for value, key in self._list)
        else:
            return KeysView(self)

    def iterkeys(self):
        """Return an iterable over the keys of the dictionary."""
        return iter(key for value, key in self._list)

    @not26
    def viewkeys(self):
        """
        In Python 2.7 and later, return a new `KeysView` of the dictionary's
        keys.

        In Python 2.6, raise a NotImplementedError.
        """
        return KeysView(self)

    def values(self):
        """
        In Python 2, return a list of the dictionary's values.

        In Python 3, return a new :class:`ValuesView` of the dictionary's
        values.  In addition to the methods provided by the built-in `view`
        the ValuesView is indexable (e.g., ``d.values()[5]``).
        """
        return list(value for value, key in self._list)

    def itervalues(self):
        """Return an iterable over the values of the dictionary."""
        return iter(value for value, key in self._list)

    @not26
    def viewvalues(self):
        """
        In Python 2.7 and later, return a new `ValuesView` of the dictionary's
        values.

        In Python 2.6, raise a NotImplementedError.
        """
        return ValuesView(self)
    
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

    def bisect_left(self, value):
        """
        Similar to the ``bisect`` module in the standard library, this returns
        an appropriate index to insert *value* in PriorityDict. If *value* is
        already present in PriorityDict, the insertion point will be before (to
        the left of) any existing entries.
        """
        return self._list.bisect_left((value,))

    def bisect(self, value):
        """Same as bisect_left."""
        return self._list.bisect((value,))

    def bisect_right(self, value):
        """
        Same as `bisect_left`, but if *value* is already present in
        PriorityDict, the insertion point will be after (to the right
        of) any existing entries.
        """
        # TODO: test with multiple equal values
        return self._list.bisect_right((value, _Biggest))

    def __add__(self, that):
        """Add values from two mappings."""
        result = PriorityDict()
        result._dict.update(self._dict)
        result._dict += that
        if hexversion < 0x03000000:
            items = result._dict.iteritems()
        else:
            items = iter(result._dict.items())
        result._list.update((value, key) for key, value in items)
        return result

    def __iadd__(self, that):
        """Add values from `that` mapping."""
        # TODO: Refactor to stub generic application of operator
        if isinstance(that, PriorityDict):
            that = that._dict

        if len(that) * 3 > len(self._dict):
            self._dict += that
            self._list.clear()

            if hexversion < 0x03000000:
                items = self._dict.iteritems()
            else:
                items = iter(self._dict.items())

            self._list.update((value, key) for key, value in items)
        else:
            for key in that:
                if key in self._dict:
                    value = self._dict[key]
                    self._list.remove((value, key))

            self._dict += that

            for key in that:
                value = self._dict[key]
                self._list.add((value, key))

    def __sub__(self, that):
        """Subtract values from two mappings."""
        result = PriorityDict()
        result._dict.update(self._dict)
        result._dict -= that
        if hexversion < 0x03000000:
            items = result._dict.iteritems()
        else:
            items = iter(result._dict.items())
        result._list.update((value, key) for key, value in items)
        return result

    def __isub__(self, that):
        """Subtract values from `that` mapping."""
        if isinstance(that, PriorityDict):
            that = that._dict

        if len(that) * 3 > len(self._dict):
            self._dict -= that
            self._list.clear()

            if hexversion < 0x03000000:
                items = self._dict.iteritems()
            else:
                items = iter(self._dict.items())

            self._list.update((value, key) for key, value in items)
        else:
            for key in that:
                if key in self._dict:
                    value = self._dict[key]
                    self._list.remove((value, key))

            self._dict -= that

            for key in that:
                value = self._dict[key]
                self._list.add((value, key))

    def __and__(self, that):
        """And values from two mappings (min(v1, v2))."""
        result = PriorityDict()
        result._dict.update(self._dict)
        result._dict &= that
        if hexversion < 0x03000000:
            items = result._dict.iteritems()
        else:
            items = iter(result._dict.items())
        result._list.update((value, key) for key, value in items)
        return result

    def __iand__(self, that):
        """And values from `that` mapping (min(v1, v2))."""
        if isinstance(that, PriorityDict):
            that = that._dict

        if len(that) * 3 > len(self._dict):
            self._dict &= that
            self._list.clear()

            if hexversion < 0x03000000:
                items = self._dict.iteritems()
            else:
                items = iter(self._dict.items())

            self._list.update((value, key) for key, value in items)
        else:
            for key in that:
                if key in self._dict:
                    value = self._dict[key]
                    self._list.remove((value, key))

            self._dict &= that

            for key in that:
                value = self._dict[key]
                self._list.add((value, key))

    def __or__(self, that):
        """Or values from two mappings (max(v1, v2))."""
        result = PriorityDict()
        result._dict.update(self._dict)
        result._dict |= that
        if hexversion < 0x03000000:
            items = result._dict.iteritems()
        else:
            items = iter(result._dict.items())
        result._list.update((value, key) for key, value in items)
        return result

    def __ior__(self, that):
        """Or values from `that` mapping (max(v1, v2))."""
        if isinstance(that, PriorityDict):
            that = that._dict

        if len(that) * 3 > len(self._dict):
            self._dict |= that
            self._list.clear()

            if hexversion < 0x03000000:
                items = self._dict.iteritems()
            else:
                items = iter(self._dict.items())

            self._list.update((value, key) for key, value in items)
        else:
            for key in that:
                if key in self._dict:
                    value = self._dict[key]
                    self._list.remove((value, key))

            self._dict |= that

            for key in that:
                value = self._dict[key]
                self._list.add((value, key))

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

#TODO: views were copied from sorteddict.py

class KeysView(AbstractKeysView, Set, Sequence):
    """
    A KeysView object is a dynamic view of the dictionary's keys, which
    means that when the dictionary's keys change, the view reflects
    those changes.

    The KeysView class implements the Set and Sequence Abstract Base Classes.
    """
    def __init__(self, priority_dict):
        """
        Initialize a KeysView from a PriorityDict container as *priority_dict*.
        """
        self._list = priority_dict._list
        if version_info[0] == 2:
            self._view = priority_dict._dict.viewkeys()
        else:
            self._view = priority_dict._dict.keys()
    def __len__(self):
        """Return the number of entries in the dictionary."""
        return len(self._view)
    def __contains__(self, key):
        """
        Return True if and only if *key* is one of the underlying dictionary's
        keys.
        """
        return key in self._view
    def __iter__(self):
        """
        Return an iterable over the keys in the dictionary. Keys are iterated
        over in their sorted order.

        Iterating views while adding or deleting entries in the dictionary may
        raise a RuntimeError or fail to iterate over all entries.
        """
        return iter(key for value, key in self._list)
    def __getitem__(self, index):
        """Return the key at position *index*."""
        return self._list[index][1]
    def __reversed__(self):
        """
        Return a reversed iterable over the keys in the dictionary. Keys are
        iterated over in reverse value sort order.

        Iterating views while adding or deleting entries in the dictionary may
        raise a RuntimeError or fail to iterate over all entries.
        """
        return iter(key for value, key in reversed(self._list))
    def index(self, value, start=None, stop=None):
        """
        Return the smallest *k* such that `keysview[k] == value` and `start <= k
        < end`.  Raises `KeyError` if *value* is not present.  *stop* defaults
        to the end of the set.  *start* defaults to the beginning.  Negative
        indexes are supported, as for slice indices.
        """
        return self._list.index(value, start, stop)
    def count(self, value):
        """Return the number of occurrences of *value* in the set."""
        return 1 if value in self._view else 0
    def __eq__(self, that):
        """Test set-like equality with *that*."""
        return self._view == that
    def __ne__(self, that):
        """Test set-like inequality with *that*."""
        return self._view != that
    def __lt__(self, that):
        """Test whether self is a proper subset of *that*."""
        return self._view < that
    def __gt__(self, that):
        """Test whether self is a proper superset of *that*."""
        return self._view > that
    def __le__(self, that):
        """Test whether self is contained within *that*."""
        return self._view <= that
    def __ge__(self, that):
        """Test whether *that* is contained within self."""
        return self._view >= that
    def __and__(self, that):
        """Return a SortedSet of the intersection of self and *that*."""
        return SortedSet(self._view & that)
    def __or__(self, that):
        """Return a SortedSet of the union of self and *that*."""
        return SortedSet(self._view | that)
    def __sub__(self, that):
        """Return a SortedSet of the difference of self and *that*."""
        return SortedSet(self._view - that)
    def __xor__(self, that):
        """Return a SortedSet of the symmetric difference of self and *that*."""
        return SortedSet(self._view ^ that)
    def isdisjoint(self, that):
        """Return True if and only if *that* is disjoint with self."""
        if version_info[0] == 2:
            return not any(key in self._list for key in that)
        else:
            return self._view.isdisjoint(that)
    def __repr__(self):
        return 'SortedDict_keys({0})'.format(repr(list(self)))

class ValuesView(AbstractValuesView, Sequence):
    """
    A ValuesView object is a dynamic view of the dictionary's values, which
    means that when the dictionary's values change, the view reflects those
    changes.

    The ValuesView class implements the Sequence Abstract Base Class.
    """
    def __init__(self, sorted_dict):
        """
        Initialize a ValuesView from a SortedDict container as *sorted_dict*.
        """
        self._dict = sorted_dict
        self._list = sorted_dict._list
        if version_info[0] == 2:
            self._view = sorted_dict._dict.viewvalues()
        else:
            self._view = sorted_dict._dict.values()
    def __len__(self):
        """Return the number of entries in the dictionary."""
        return len(self._dict)
    def __contains__(self, value):
        """
        Return True if and only if *value* is on the underlying dictionary's
        values.
        """
        return value in self._view
    def __iter__(self):
        """
        Return an iterator over the values in the dictionary.  Values are
        iterated over in sorted order of the keys.

        Iterating views while adding or deleting entries in the dictionary may
        raise a `RuntimeError` or fail to iterate over all entries.
        """
        return iter(self._dict[key] for key in self._list)
    def __getitem__(self, index):
        """
        Efficiently return value at *index* in iteration.

        Supports slice notation and negative indexes.
        """
        if isinstance(index, slice):
            return [self._dict[key] for key in self._list[index]]
        else:
            return self._dict[self._list[index]]
    def __reversed__(self):
        """
        Return a reverse iterator over the values in the dictionary.  Values are
        iterated over in reverse sort order of the keys.

        Iterating views while adding or deleting entries in the dictionary may
        raise a `RuntimeError` or fail to iterate over all entries.
        """
        return iter(self._dict[key] for key in reversed(self._list))
    def index(self, value):
        """
        Return index of *value* in self.

        Raises ValueError if *value* is not found.
        """
        for idx, val in enumerate(self):
            if value == val:
                return idx
        else:
            raise ValueError
    def count(self, value):
        """Return the number of occurrences of *value* in self."""
        if version_info[0] == 2:
            return sum(1 for val in self._dict.itervalues() if val == value)
        else:
            return sum(1 for val in self._dict.values() if val == value)
    def __lt__(self, that):
        raise TypeError
    def __gt__(self, that):
        raise TypeError
    def __le__(self, that):
        raise TypeError
    def __ge__(self, that):
        raise TypeError
    def __and__(self, that):
        raise TypeError
    def __or__(self, that):
        raise TypeError
    def __sub__(self, that):
        raise TypeError
    def __xor__(self, that):
        raise TypeError
    def __repr__(self):
        return 'SortedDict_values({0})'.format(repr(list(self)))

class ItemsView(AbstractItemsView, Set, Sequence):
    """
    An ItemsView object is a dynamic view of the dictionary's ``(key,
    value)`` pairs, which means that when the dictionary changes, the
    view reflects those changes.

    The ItemsView class implements the Set and Sequence Abstract Base Classes.
    However, the set-like operations (``&``, ``|``, ``-``, ``^``) will only
    operate correctly if all of the dictionary's values are hashable.
    """
    def __init__(self, sorted_dict):
        """
        Initialize an ItemsView from a SortedDict container as *sorted_dict*.
        """
        self._dict = sorted_dict
        self._list = sorted_dict._list
        if version_info[0] == 2:
            self._view = sorted_dict._dict.viewitems()
        else:
            self._view = sorted_dict._dict.items()
    def __len__(self):
        """Return the number of entries in the dictionary."""
        return len(self._view)
    def __contains__(self, key):
        """
        Return True if and only if *key* is one of the underlying dictionary's
        items.
        """
        return key in self._view
    def __iter__(self):
        """
        Return an iterable over the items in the dictionary. Items are iterated
        over in their sorted order.

        Iterating views while adding or deleting entries in the dictionary may
        raise a RuntimeError or fail to iterate over all entries.
        """
        return iter((key, self._dict[key]) for key in self._list)
    def __getitem__(self, index):
        """Return the item as position *index*."""
        if isinstance(index, slice):
            return [(key, self._dict[key]) for key in self._list[index]]
        else:
            key = self._list[index]
            return (key, self._dict[key])
    def __reversed__(self):
        """
        Return a reversed iterable over the items in the dictionary. Items are
        iterated over in their reverse sort order.

        Iterating views while adding or deleting entries in the dictionary may
        raise a RuntimeError or fail to iterate over all entries.
        """
        return iter((key, self._dict[key]) for key in reversed(self._list))
    def index(self, key, start=None, stop=None):
        """
        Return the smallest *k* such that `itemssview[k] == key` and `start <= k
        < end`.  Raises `KeyError` if *key* is not present.  *stop* defaults
        to the end of the set.  *start* defaults to the beginning.  Negative
        indexes are supported, as for slice indices.
        """
        pos = self._list.index(key[0], start, stop)
        if key[1] == self._dict[key[0]]:
            return pos
        else:
            raise ValueError
    def count(self, item):
        """Return the number of occurrences of *item* in the set."""
        key, value = item
        return 1 if key in self._dict and self._dict[key] == value else 0
    def __eq__(self, that):
        """Test set-like equality with *that*."""
        return self._view == that
    def __ne__(self, that):
        """Test set-like inequality with *that*."""
        return self._view != that
    def __lt__(self, that):
        """Test whether self is a proper subset of *that*."""
        return self._view < that
    def __gt__(self, that):
        """Test whether self is a proper superset of *that*."""
        return self._view > that
    def __le__(self, that):
        """Test whether self is contained within *that*."""
        return self._view <= that
    def __ge__(self, that):
        """Test whether *that* is contained within self."""
        return self._view >= that
    def __and__(self, that):
        """Return a SortedSet of the intersection of self and *that*."""
        return SortedSet(self._view & that)
    def __or__(self, that):
        """Return a SortedSet of the union of self and *that*."""
        return SortedSet(self._view | that)
    def __sub__(self, that):
        """Return a SortedSet of the difference of self and *that*."""
        return SortedSet(self._view - that)
    def __xor__(self, that):
        """Return a SortedSet of the symmetric difference of self and *that*."""
        return SortedSet(self._view ^ that)
    def isdisjoint(self, that):
        """Return True if and only if *that* is disjoint with self."""
        if version_info[0] == 2:
            for key, value in that:
                if key in self._dict and self._dict[key] == value:
                    return False
            return True
        else:
            return self._view.isdisjoint(that)
    def __repr__(self):
        return 'SortedDict_items({0})'.format(repr(list(self)))
