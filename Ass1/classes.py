"""Module containing classes for storing and comparing Names."""

import doctest
from stats import StatCounter, NAME_COMPS

NAME_COMP_ERROR = "Can only compare Names with other Names"
NAME_CREATE_ERROR = "You can only create Names from str's"


def c_mul(a, b):
    """Used for hashing - don't worry how/why"""
    return (int(a) * int(b)) & 0xFFFFFFFF


class Name:
    """A wrapped string representing a name.
    Name objects count comparisons between themselves and other names
    via the stats class
    >>> x = Name('Lee')
    >>> y = Name('Lee')
    >>> x == y
    True
    >>> x != y
    False
    >>> x > y
    False
    >>> x >= y
    True
    >>> x < y
    False
    >>> x <= y
    True
    >>> hash(x)
    959489702
    >>> hash(y)
    959489702
    >>> z = Name('Dee')
    >>> hash(z)
    1590222686
    >>> t = Name('Tom')
    >>> hash(t)
    386756888
    >>> name_list = [x, z]
    >>> print(name_list)
    [Name('Lee'), Name('Dee')]
    >>> print(name_list[0])
    <Lee>
    >>> print(name_list[1])
    <Dee>
    """

    # class variables
    # whenever a Name is hashed this count will be incremented by the __hash__ method
    _hashes_used = 0

    def __init__(self, base):
        """Names should only be made out of str objects, ie, base must be a str
        If you get errors then make sure you aren't trying to
        make a Name out of a Name!
        """
        if isinstance(base, str):
            self._name = base
        else:
            raise TypeError(NAME_CREATE_ERROR)

    def __eq__(self, j):
        if not isinstance(j, Name):
            raise TypeError(NAME_COMP_ERROR)
        else:
            StatCounter.increment(NAME_COMPS)
            return self._name == j._name

    def __le__(self, j):
        if not isinstance(j, Name):
            raise TypeError(NAME_COMP_ERROR)
        else:
            StatCounter.increment(NAME_COMPS)
            return self._name <= j._name

    def __ne__(self, j):
        if not isinstance(j, Name):
            raise TypeError(NAME_COMP_ERROR)
        else:
            StatCounter.increment(NAME_COMPS)
            return self._name != j._name

    def __lt__(self, j):
        if not isinstance(j, Name):
            raise TypeError(NAME_COMP_ERROR)
        else:
            StatCounter.increment(NAME_COMPS)
            return self._name < j._name

    def __gt__(self, j):
        if not isinstance(j, Name):
            raise TypeError(NAME_COMP_ERROR)
        else:
            StatCounter.increment(NAME_COMPS)
            return self._name > j._name

    def __ge__(self, j):
        if not isinstance(j, Name):
            raise TypeError(NAME_COMP_ERROR)
        else:
            StatCounter.increment(NAME_COMPS)
            return self._name >= j._name

    def __repr__(self):
        return f"Name({repr(self._name)})"

    def __str__(self):
        """Returns a string in the form <self._name>
        This allows you to distinguish between Name objects
        and plain strings when printing.
        """
        return f"<{self._name}>"

    def __hash__(self):
        """Called by hash(a_name) to get a raw hash value for the given name.
        You should use hash(a_name) instead of a_name.__hash__().
        """
        Name._hashes_used += 1
        if self._name is None:
            return 0
        value = ord(self._name[0]) << 7
        for char in self._name:
            value = c_mul(1000003, value) ^ ord(char)
        value = value ^ len(self._name)
        if value == -1:
            value = -2
        # The result is trimmed down to 31 bits (plus a sign bit) to give
        # consistent results on 32 and 64 bit systems
        # Otherwise hash() will implicitly do this based on the Python build
        # see https://docs.python.org/3/reference/datamodel.html#object.__hash__
        value = value % 0b0111_1111_1111_1111_1111_1111_1111_1111
        return value

    # the following are used for testing
    @classmethod
    def get_hashes(cls):
        return cls._hashes_used

    @classmethod
    def reset_hashes(cls):
        cls._hashes_used = 0


if __name__ == "__main__":
    # won't run when importing this module
    doctest.testmod()
