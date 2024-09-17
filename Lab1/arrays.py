""" Array classes for Lab 1.
NOTE: the LinearArray doctests will fail until your implement the find_index method"""
import doctest


# ------------------------------------------------------------------------
class LinearArray():
    """Implements an array using an un-ordered Python list.

    >>> straighty = LinearArray()
    >>> straighty.insert(12)
    >>> straighty.insert(82)
    >>> straighty.insert(45)
    >>> straighty.insert(11)
    >>> print(straighty)
    0 , 12
    1 , 82
    2 , 45
    3 , 11
    <BLANKLINE>
    >>> print(straighty.find_index(45))
    2
    >>> print(straighty.comparisons)
    3
    >>> print(straighty.find_index(7))
    None
    >>> print(straighty.comparisons)
    4
    >>> print(straighty.find_index(2))
    None
    >>> print(straighty.comparisons)
    4
    >>> print(straighty.find_index(12))
    0
    >>> print(straighty.comparisons)
    1
    >>> straighty.remove(45)
    >>> print(straighty.comparisons)
    3
    """

    def __init__(self):
        self.data = list()  # Create the list to store the data
        self.comparisons = 0  # Reset comparison counter

    def insert(self, value):
        """Adds an item to the end of the array"""
        # Add the item to the end of the data list
        self.data.append(value)
        # obviously this didn't use any comparisons
        self.comparisons = 0

    def remove(self, value):
        """Removes the first occurrence of value in the array."""
        # Look for the index in the list that
        # contains the element to delete
        index = self.find_index(value)

        # If we've found the item...
        if index is not None:
            # Delete it from the list
            del self.data[index]
        # otherwise do nothing as it wasn't in the list...

    def contains(self, value):
        """Returns True if the array contains the value, else returns False."""
        return self.find_index(value) is not None

    def find_index(self, value):
        """
        Finds the index of the given value in the data list.
        Returns either the index of the item in the list, or None if
        the item doesn't exist.
        Keeps track of the number of comparisons between value and
        items in the list via self.comparisons.
        For example, you don't need to count any index comparisons you
        might make as part of a while statement.
        """
        # Counter for how many comparisons are done is set to zero
        self.comparisons = 0
        for i, val in enumerate(self.data):
            self.comparisons += 1
            if val == value:
                return i
            else:
                pass
        return None
        # Loop through each item in the data list
        # Add one to comparisons for each comparison
        # involving a list element
            # If the item is equal to our search value
            # return the index this item is at
        # If we loop through everything and haven't found
        # the item, return None

    def __str__(self):
        """
        Prints out all the values in the array
        """
        string = ''
        for i, value in enumerate(self.data):
            string += f'{i} , {value}\n'
        return string


# ------------------------------------------------------------------------
class SortedArray():

    """Implements an array using a Python list, but stores the items in
    sorted order (rather than the order they are inserted).
    >>> speedy = SortedArray()
    >>> speedy.insert(12)
    >>> speedy.insert(30)
    >>> speedy.insert(82)
    >>> speedy.insert(45)
    >>> speedy.insert(11)
    >>> print(speedy.comparisons)
    3
    >>> print(speedy)
    0 , 11
    1 , 12
    2 , 30
    3 , 45
    4 , 82
    <BLANKLINE>
    >>> print(speedy.find_index(11))
    0
    >>> print(speedy.comparisons)
    5
    >>> print(speedy.find_index(7))
    None
    >>> print(speedy.comparisons)
    6
    >>> print(speedy.find_index(2))
    None
    >>> print(speedy.comparisons)
    6
    >>> print(speedy.find_index(45))
    3
    >>> print(speedy.comparisons)
    5
    >>> speedy.remove(45)
    >>> print(speedy.comparisons)
    5

    """

    def __init__(self):
        self.data = list()
        self.comparisons = 0

    def insert(self, value):
        """Inserts an item in to the array in its sorted position"""
        self.comparisons = 0
        # Find the correct index to insert value using a binary search
        lower_bound = 0
        upper_bound = len(self.data)
        index = 0
        # When these cross, they're at the index the item should be at
        while lower_bound < upper_bound:
            index = (lower_bound + upper_bound) // 2
            self.comparisons += 1
            if self.data[index] < value:
                lower_bound = index + 1  # Look in the upper half
            else:
                upper_bound = index     # Look in the lower half

        # the following will use the list insert method to insert
        # into the self.data list - think about how you insert
        # into a list. help(list.insert) will be helpful as ever :)
        # ie, it won't be calling this SortedArray insert method...
        self.data.insert(lower_bound, value)

    def remove(self, value):
        """Removes the first occurrence of value in the array."""
        # Find the index to remove
        index = self.find_index(value)
        # If we've found the item...
        if index is not None:
            # Delete it from the list
            # (this will shuffle all of the higher items down for us)
            del self.data[index]

    def contains(self, value):
        """Returns True if the array contains the value, else returns False"""
        return self.find_index(value) is not None

    def find_index(self, value):
        """ Finds the index of the given value in the data list.
        Returns either the index of the item in the list, or None if
        the item doesn't exist.
        Keeps track of the number of comparisons between value and
        items in the list via self.comparisons.
        You don't need to count any other comparisons, eg,
        don't count lower_bound < upper_bound.
        """
        self.comparisons = 0
        lower_bound = 0
        upper_bound = len(self.data)
        while lower_bound < upper_bound:
            index = (lower_bound + upper_bound) // 2
            self.comparisons += 1
            if self.data[index] == value:  # Found it!
                return index
            self.comparisons += 1
            if self.data[index] < value:
                lower_bound = index + 1  # Look in the upper half
            else:
                upper_bound = index      # Look in the lower half
        # If we haven't found it by now, it doesn't exist
        return None

    def __str__(self):
        """
        Prints out all the values in the array
        """
        string = ''
        for i, value in enumerate(self.data):
            string += f'{i} , {value}\n'
        return string



# ------------------------------------------------------------------------
class BitVectorArray():

    """Implements an array using a variation on a bit vector (bitmap).

    For example the following values in data would indicate the the
    BitVectorArray instance contains the number 4 and two number 6's

    index:         0 1 2 3 4 5 6 ...
    data[index]:   0 0 0 0 1 0 2 ...

    Try the following:
    >>> bva = BitVectorArray(10)
    >>> bva.insert(10)
    >>> bva.insert(4)
    >>> bva.insert(2)
    >>> bva.insert(4)
    >>> print(bva)
    0, 0
    1, 0
    2, 1
    3, 0
    4, 2
    5, 0
    6, 0
    7, 0
    8, 0
    9, 0
    10, 1

    """

    def __init__(self, max_value):
        """
        Creates a new BitVectorArray.
        maxValue is the largest integer value that can be stored in this array.
        Sets all the values in data to 0.
        """
        self.data = [0 for n in range(max_value + 1)]
        self.comparisons = 0

    def remove(self, value):
        """Removes an occurrence of the value in the array."""
        self.comparisons = 0
        if self.data[value]:
            self.data[value] -= 1

    def insert(self, value):
        """ Basically data[value] will count the number of times
        the value has been added to the array
        """
        self.data[value] += 1

    def contains(self, value):
        """Returns True if the array contains the value, else returns False"""
        return self.data[value] > 0

    def __str__(self):
        """Prints out all the values in the array."""
        string = ''
        for i, value in enumerate(self.data):
            string += f'{i}, {value}\n'
        return string.strip()


if __name__ == '__main__':
    # This code won't run if this module is imported
    # It only runs if you run this module, eg, by hitting play in Wing
    # Notes:
    # The LinearArray tests will fail until
    #      you implement the find_index method
    # The SortedArray will fail until you count comparisons
    # Feel free to practice writing more doctests :)

    doctest.run_docstring_examples(LinearArray, None)

    # You can uncomment the SortedArray tests until you
    # are ready to run them
    # doctest.run_docstring_examples(SortedArray, None)

    # or use the following to run all the tests at once
    # doctest.testmod()
