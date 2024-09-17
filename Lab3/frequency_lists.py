"""FrequencyList classes and testing routines.
Work through the lab handout to find out what you are doing..."""

import time
import re
import os
import doctest
from unicodedata import category
import matplotlib.pyplot as plt

os.environ['TERM'] = 'linux'  # Suppress ^[[?1034h


# -------------------------------------------------------------------------
class FreqNode(object):
    """Stores an item, frequency pair.

    Basically a FreqNode object is a node in the frequency list.
    Each FreqNode holds an item, the frequency for the item,
    and a pointer to the next FreqNode object (or None).

    >>> f = FreqNode('c', 2)
    >>> f.item
    'c'
    >>> f.frequency
    2
    >>> print(f)
    'c' = 2
    """

    def __init__(self, item, frequency=1):
        self.item = item
        self.frequency = frequency
        self.next_node = None

    def increment(self):
        """ Add one to the frequency count for this item """
        self.frequency += 1

    def __str__(self):
        return f"'{self.item}' = {self.frequency}"


# -------------------------------------------------------------------------
class FreqList(object):
    """Stores a linked list of FreqNode objects.
    NOTE: This is a parent class for Unsorted, NicerUnSorted & Sorted FreqLists
    """

    def __init__(self):
        self.head = None
        self.freq_list_type = 'Generic parent'

    def add(self, item):
        """Will be implemented by child classes. Don't write anything here.
        This will add an item with frequency=1 if item not in list,
        otherwise it will increment the frequency count for the item.
        """
        pass

    def get_item_frequency(self, item):
        """Returns Frequency of item, if found else returns 0.

        **** NOTE: Don't use this when writing your add methods. ****

        That is, you should scan through the list directly when adding.
        Using this method to check for existence of an item will be
        very inefficient... think about why.
        """
        current = self.head
        while current is not None:
            if current.item == item:
                return current.frequency
            current = current.next_node
        return 0

    def get_xy_for_plot(self):
        """ Returns two lists that can be used for plotting
        items and frequencies.
        The first contains the items and the second contains the frequecies.
        """
        x_values = []
        y_values = []
        curr_item = self.head
        while curr_item is not None:
            # use repr of items so that spaces show, eg, 'e '
            x_values.append(repr(curr_item.item))
            y_values.append(curr_item.frequency)
            curr_item = curr_item.next_node
        return x_values, y_values

    def _max_index_width(self):
        """
        Returns widest index width + 2
        For example, if there are 100 items in the list
        then 100 is the maximum item number and it is 3 characters wide,
        so set the width for the index column to 5
        """
        length = len(self)
        return len(str(length)) + 2

    def __len__(self):
        """Returns the number of nodes in the freq. list. Zero if empty."""
        current = self.head
        length = 0
        while current is not None:
            length += 1
            current = current.next_node
        return length

    def __str__(self):
        """Returns a multiline table containing the items together
           with their frequencies."""
        result = self.freq_list_type + '\n'
        result += '-' * 35 + '\n'
        line_strs = []
        current_node = self.head
        max_index_width = self._max_index_width()
        node_num = 1
        while current_node is not None:
            line_str = f'{node_num:>{max_index_width}}:  {str(current_node)}'
            line_strs.append(line_str)
            current_node = current_node.next_node
            node_num += 1
        return result + '\n'.join(line_strs)


# -------------------------------------------------------------------------
class UnsortedFreqList(FreqList):
    """FreqList that adds new items to the front/head of the linked list.

    UnsortedFreqList objects get to use the __len__  methods etc,
    of the FreqList class, because this class is inheriting from FreqList.
    This saves you having to define them again :)

    TO DO -------> All you need to do is write an add method
    """

    def __init__(self):
        super().__init__()
        self.freq_list_type = 'Unsorted Frequency List'

    def add(self, item):
        """
        Updates the count for a given item/letter.
        If the given item is already in the list, the frequency for that
        item is incremented by 1.
        If not in the list then the item is put into a new node (with freq 1)
        and the node is inserted at the start of the frequency list.

        >>> f = UnsortedFreqList()
        >>> f.add('a')
        >>> print(f)
        Unsorted Frequency List
        -----------------------------------
          1:  'a' = 1
        >>> f.add('b')
        >>> print(f)
        Unsorted Frequency List
        -----------------------------------
          1:  'b' = 1
          2:  'a' = 1
        >>> f.add('a')
        >>> print(f)
        Unsorted Frequency List
        -----------------------------------
          1:  'b' = 1
          2:  'a' = 2
        >>> f.add('c')
        >>> print(f)
        Unsorted Frequency List
        -----------------------------------
          1:  'c' = 1
          2:  'b' = 1
          3:  'a' = 2
        """
        current = self.head

        # Traverse the list to find the item
        while current is not None:
            if current.item == item:
                current.increment()
                return
            current = current.next_node

        # If item is not found, add a new node at the head of the list
        new_node = FreqNode(item)
        new_node.next_node = self.head
        self.head = new_node


# -------------------------------------------------------------------------
class NicerUnsortedFreqList(FreqList):
    """FreqList that adds new items at the end of the list.

    TO DO -------> All you need to do is write an add method
    """

    def __init__(self):
        super().__init__()
        self.freq_list_type = 'Nicer Unsorted Frequency List'

    def add(self, item):
        """
        If the given `letter` is already in the list, the frequency is
        incremented by 1.  If not in list, the item is added to the end of the
        list with a frequency of 1.

        >>> f = NicerUnsortedFreqList()
        >>> f.add('a')
        >>> print(f)
        Nicer Unsorted Frequency List
        -----------------------------------
          1:  'a' = 1
        >>> f.add('b')
        >>> print(f)
        Nicer Unsorted Frequency List
        -----------------------------------
          1:  'a' = 1
          2:  'b' = 1
        >>> f.add('a')
        >>> print(f)
        Nicer Unsorted Frequency List
        -----------------------------------
          1:  'a' = 2
          2:  'b' = 1
        >>> f.add('c')
        >>> print(f)
        Nicer Unsorted Frequency List
        -----------------------------------
          1:  'a' = 2
          2:  'b' = 1
          3:  'c' = 1
        """
        current = self.head
        previous = None

        # Traverse the list to find the item
        while current is not None:
            if current.item == item:
                current.increment()
                return
            previous = current
            current = current.next_node

        new_node = FreqNode(item)
        if previous is None:
            self.head = new_node
        else:
            previous.next_node = new_node


# -------------------------------------------------------------------------
class SortedFreqList(FreqList):
    """FreqList that keeps items in order, sorted by their frequencies.

    TO DO -------> All you need to do is write an add method
    """

    def __init__(self):
        super().__init__()
        self.freq_list_type = 'Sorted Frequency List'

    def _insert_in_order(self, freq_node):
        """ Takes a FreqNode and inserts in to the list so that
        items are sorted from largest to smallest.

        NOTE: This method does not work on an empty list.
        This method should only be called from the add method,
        see the add method docstring for information on how to use this method.

        ***** DO NOT change this method! *****
        """
        # so we don't have to lookup each time
        freq_of_item = freq_node.frequency

        # check to see if larger than first freq in list
        if freq_of_item > self.head.frequency:
            freq_node.next_node = self.head
            self.head = freq_node
        else:
            curr_freq = self.head
            inserted = False
            while curr_freq.next_node is not None and not inserted:
                if freq_of_item > curr_freq.next_node.frequency:
                    # insert here
                    freq_node.next_node = curr_freq.next_node
                    curr_freq.next_node = freq_node
                    inserted = True
                else:
                    curr_freq = curr_freq.next_node
            # got to end and didn't find
            if not inserted:
                freq_node.next_node = None  # as now at end of list
                curr_freq.next_node = freq_node

    def add(self, item):
        """
        Updates the count for a given item/letter. See below for how to do this:

        If the list is empty then make a new FreqNode and insert it at head.

        If the item is not already in freq list then add the given
        item with a frequency of 1 as a FreqNode object to the end of the list.

        If the given new item is already in the list:
           The frequency is incremented by 1.
           If needed (ie, the freq is now greater than the previous node),
             the node is unlinked and then re-inserted
             into its sorted position - using _insert_in_order.

        Note: You should do this with the normal singly linked nodes.
              As an exercise you might want to rewrite using
              a doubly linked list, which makes insertion easier.



        >>> x = SortedFreqList()
        >>> x.add('t')
        >>> x.add('t')
        >>> print(x)
        Sorted Frequency List
        -----------------------------------
          1:  't' = 2
        >>> f = SortedFreqList()
        >>> f.add('a')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'a' = 1
        >>> f.add('b')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'a' = 1
          2:  'b' = 1
        >>> f.add('b')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'b' = 2
          2:  'a' = 1
        >>> f.add('c')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'b' = 2
          2:  'a' = 1
          3:  'c' = 1
        >>> f.add('a')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'b' = 2
          2:  'a' = 2
          3:  'c' = 1
        >>> f.add('c')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'b' = 2
          2:  'a' = 2
          3:  'c' = 2
        >>> f.add('c')
        >>> f.add('d')
        >>> f.add('d')
        >>> f.add('e')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'c' = 3
          2:  'b' = 2
          3:  'a' = 2
          4:  'd' = 2
          5:  'e' = 1
        >>> f.add('e')
        >>> f.add('e')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'c' = 3
          2:  'e' = 3
          3:  'b' = 2
          4:  'a' = 2
          5:  'd' = 2
        >>> f.add('c')
        >>> print(f)
        Sorted Frequency List
        -----------------------------------
          1:  'c' = 4
          2:  'e' = 3
          3:  'b' = 2
          4:  'a' = 2
          5:  'd' = 2
        """
        # make sure you read the docstring for this method!
        if self.head is None:
            self.head = FreqNode(item)
        else:
            current = self.head
            previous = None
            found = False# Traverse the list to find the item
            while current is not None:
                if current.item == item:
                    current.increment()
                    found = True
                    break
                previous = current
                current = current.next_node

            if found:
                if previous and current.frequency > previous.frequency:
                    if previous is not None:
                        previous.next_node = current.next_node
                    self._insert_in_order(current)
            else:
                new_node = FreqNode(item)
                self._insert_in_order(new_node)


def run_full_doctests(with_verbose=True):
    # run all the doctests  -- comment this out if you are running individual
    # tests
    result = doctest.testmod()
    if with_verbose:
        print(result)


def main():
    """ The place to run doctests and other tests """
    # Uncomment doctests as needed...
    # If everything passes you just get a quick summary
    # otherwise failures will be printed.

    # Note: the doctests test your classes with some simple examples
    # To process txt files use the run_tests function.

    # change to False to get less doctest output
    with_verbose = True

    # Individual tests:
    # Uncomment ones that you want to run individually
    # doctest.run_docstring_examples(UnsortedFreqList.add, None, verbose=with_verbose)
    # doctest.run_docstring_examples(NicerUnsortedFreqList.add, None, verbose=with_verbose)
    # doctest.run_docstring_examples(SortedFreqList.add, None, verbose=with_verbose)

    # Comment out the call to run_full_doctests if you just want to run one of the above
    # invidual class tests
    run_full_doctests(with_verbose)


if __name__ == '__main__':
    main()
