""" Note we have called this module queue122.py
to avoid a clash with the inbuilt module called queue.
"""
import doctest

# uncomment the following two lines if you have problems with strange characters
# import os
# os.environ['TERM'] = 'linux' # Suppress ^[[?1034h


class Queue(object):
    """Implements a Queue using a Python list.
    Internally the queue is stored as plain Python list.
    The front of the queue is at index 0 and rear is last item in the list.
    _data is a private variable inside each queue instance and shouldn't
    be accessed from outside the queue (eg, don't do q._data.dequeue(), you should
    be using q.dequeue()
    >>> q = Queue()
    >>> q.enqueue('a')
    >>> q.dequeue()
    'a'
    >>> q.enqueue('a')
    >>> q.enqueue('b')
    >>> len(q)
    2
    >>> q.dequeue()
    'a'
    >>> len(q)
    1
    >>> q.dequeue()
    'b'
    >>> q.dequeue()
    Traceback (most recent call last):
    ...
    IndexError: Can't dequeue from an empty queue!
    >>> q.enqueue('a')
    >>> q.enqueue('b')
    >>> q.enqueue('c')
    >>> q.enqueue('a')
    >>> q.enqueue('d')
    >>> print(q)
    Front -> ['a', 'b', 'c', 'a', 'd'] <- Rear
    >>> q.dequeue()
    'a'
    >>> print(q)
    Front -> ['b', 'c', 'a', 'd'] <- Rear
    """

    def __init__(self):
        """ Creates an empty queue """
        self._data = []

    def enqueue(self, item):
        """Add an item onto the rear of the queue."""
        self._data.append(item)

    def dequeue(self):
        """Remove an item from the front of the queue and return it.
        Raise IndexError if empty."""
        if self.is_empty():
            raise IndexError('Can\'t dequeue from an empty queue!')
        else:
            return self._data.pop(0)

    def is_empty(self):
        """ Returns True if the queue is empty """
        return len(self) == 0

    def __len__(self):
        """ Returns the length of the queue """
        return len(self._data)

    def __str__(self):
        """ Returns a simple string showing the Queue """
        return "Front -> " + repr(self._data) + " <- Rear"

    def __repr__(self):
        """ Returns a representation, simply the __str__
        This is useful for displaying the Queue in the shell
        """
        return str(self)


if __name__ == '__main__':

    # failed doctests will show you what you need to fix/write
    # If everything works then the doctests will output nothing...
    doctest.testmod()   # use verbose=1 if you want to always get some output

