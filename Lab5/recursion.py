from random import *
from turtle import *


class Node:

    def __init__(self, item):
        self.item = item
        self.next_node = None


def add_item_to_list(first_node, item):
    """
    Adds item to end of linked list.
    first_node is the first node in the list.
    Note: this is a non-recursive function
    It's used to help us build lists for testing.
    Think about how to make it recursive :)
    """
    if first_node is None:
        # the list needs a first node
        # initialise a first node with first_node = Node(item)
        # then call add_item_to_list to add another node
        raise IndexError("None doesn't have a .next_node")
    else:
        new_node = Node(item)
        current_node = first_node
        # traverse list until at last node
        while current_node.next_node is not None:
            current_node = current_node.next_node
        # set last node's next pointer to point to the new node
        current_node.next_node = new_node


def fib_recursive(n):
    """Returns the n'th Fibonacci number.
    n must be an integer that is >= 1.
    >>> fib_recursive(1)
    1
    >>> fib_recursive(2)
    1
    >>> fib_recursive(3)
    2
    >>> fib_recursive(4)
    3
    >>> fib_recursive(9)
    34
    """
    if n == 1 or n == 2:
        return 1
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    """Returns the n'th Fibonacci number.
    n must be an integer that is >= 1
    >>> fib_iterative(1)
    1
    >>> fib_iterative(2)
    1
    >>> fib_iterative(3)
    2
    >>> fib_iterative(4)
    3
    >>> fib_iterative(9)
    34
    """
    if n == 1 or n == 2:
        return 1
    else:
        # n >= 3 so start with fib of 1 an fib of 2
        # as the last two terms
        # That is, calculate fib 3 first.
        fib_n_minus2 = 1
        fib_n_minus1 = 1
        for i in range(3, n + 1):
            curr_fib = fib_n_minus1 + fib_n_minus2
            fib_n_minus2 = fib_n_minus1
            fib_n_minus1 = curr_fib
        return curr_fib


def print_fibonacci_sequence(n):
    """
    Prints Fibonacci numbers from the first up to the nth number.

    >>> print_fibonacci_sequence(9)
    1
    1
    2
    3
    5
    8
    13
    21
    34
    """
    if n == 1:
        print(fib_recursive(1))
    else:
        # print all the fib numbers up to n-1
        print_fibonacci_sequence(n - 1)
        # print the nth fib number
        print(fib_recursive(n))


def gcd(a, b):
    """Computes the greatest common divisor of a and b."""
    if b == 0:
        return a
    elif a < b:
        return gcd(b, a)
    else:
        return gcd(a - b, b)


def str_length(s):
    """
    Calculates the length of a string.
    Definitely not the best way of doing this!
    Think about how much space all the sub lists will take up.
    """
    if s == "":
        return 0
    return 1 + str_length(s[1:])


def random_tree(size, level):
    """
    Draws a funky fractal tree.
    Feel free to experiment with parameters...
    """
    if level != 0:
        forward(random() * size)
        x = pos()
        angle = random() * 20
        right(angle)
        random_tree(size * 0.8, level - 1)
        setpos(x)
        left(angle)
        angle = random() * -20
        right(angle)
        random_tree(size * 0.8, level - 1)
        left(angle)
        setpos(x)


# -------------------------------------------------------------------------
# Functions for students to implement
# -------------------------------------------------------------------------


def factorial(n):
    """
    Returns n!

    n must be >= 0
    Feel free to raise an exception if n is not valid.

    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(5)
    120
    """
    # ---start student section---
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
    # ===end student section===


# -------------- power to the recursionists! -----------------------------


def slow_power(x, n):
    """Computes x to the power of n, the slow way!
    Named slow_power to distinguish it from quick_power, which you will write later.
    >>> slow_power(2, 2)
    4
    >>> slow_power(2, 3)
    8
    """
    if n == 0:
        return 1
    else:
        return x * slow_power(x, n - 1)


def quick_power(x, n):
    """
    Computes x ^ n where n is an integer and is >= 0
    Feel free to raise an exception if n is not valid.
    NOTES:
    - You need to write the doc test for the base case.
    - You shouldn't use the ** operator in your function
    - You shouldn't use the slow_power function either
    - Remember n squared is simply n * n
        + quick_power should only call itself once...
    >>> quick_power(2,3)
    8
    >>> quick_power(2, 8)
    256
    >>> quick_power(2, 16)
    65536
    >>> quick_power(2, 64)
    18446744073709551616
    >>> quick_power(2, 128)
    340282366920938463463374607431768211456
    >>> quick_power(4, 64)
    340282366920938463463374607431768211456
    >>> quick_power(10, 32)
    100000000000000000000000000000000
    >>> quick_power(8, 32)
    79228162514264337593543950336
    """
    # ---start student section---
    if n == 0:
        return 1
    if n % 2 == 0:
        return quick_power(x * x, n // 2)
    else:
        return x * quick_power(x, n - 1)
    # ===end student section===


# -------------- Recursive linked lists ----------------------


def linked_list_length(list_node):  # Q15
    """
    Returns the number of nodes in a linked list,
    0 if list is empty.
    >>> first_node = None
    >>> print(linked_list_length(first_node))
    0
    >>> first_node = Node(1)
    >>> print(linked_list_length(first_node))
    1
    >>> add_item_to_list(first_node, 2)
    >>> print(linked_list_length(first_node))
    2
    >>> add_item_to_list(first_node, 3)
    >>> print(linked_list_length(first_node))
    3
    >>> add_item_to_list(first_node, 4)
    >>> print(linked_list_length(first_node))
    4
    >>> add_item_to_list(first_node, 10)
    >>> print(linked_list_length(first_node))
    5
    """
    # Note: you shouldn't be using a while loop here.
    # Think of the length of the list as the length of
    # the first node (ie 1) plus the length of the rest of the list.
    # Remember you should be using recursion so your function should
    # call linked_list_length at some stage!
    # ---start student section---
    if list_node is None:
        return 0
    else:
        return 1 + linked_list_length(list_node.next_node)
    # ===end student section===


def linked_list_print(list_node):
    """
    Prints the items in the list, from the first to the last, one item per line.
    This function shouldn't return anything!
    If the list is empty then nothing is printed.
    >>> first_node = None
    >>> linked_list_print(first_node)   # nothing should be printed
    >>> first_node = Node(1)
    >>> linked_list_print(first_node)
    1
    >>> add_item_to_list(first_node, 2)
    >>> linked_list_print(first_node)
    1
    2
    >>> add_item_to_list(first_node, 3)
    >>> linked_list_print(first_node)
    1
    2
    3
    >>> add_item_to_list(first_node, 4)
    >>> linked_list_print(first_node)
    1
    2
    3
    4
    >>> nothing = None
    >>> linked_list_print(nothing)   # should not print anything
    >>> first_node = Node(100)
    >>> linked_list_print(first_node)
    100
    >>> returned = linked_list_print(first_node)
    100
    >>> print(returned)
    None
    """
    # Note: you shouldn't be using a while loop here.
    # Remember you should be using recursion so your function should
    # call linked_list_print at some stage!
    # ---start student section---
    if list_node is not None:
        print(list_node.item)
        linked_list_print(list_node.next_node)
    # ===end student section===


def linked_list_reverse_print(list_node):
    """
    Prints the items in the list in reverse, one item per line.
    Shouldn't return anything.
    Should print nothing if the list is empty.

    >>> first_node = Node(1)
    >>> linked_list_reverse_print(first_node)
    1
    >>> add_item_to_list(first_node, 2)
    >>> linked_list_reverse_print(first_node)
    2
    1
    >>> add_item_to_list(first_node, 3)
    >>> linked_list_reverse_print(first_node)
    3
    2
    1
    >>> add_item_to_list(first_node, 4)
    >>> linked_list_reverse_print(first_node)
    4
    3
    2
    1
    >>> linked_list_reverse_print(None)   # should print nothing
    """
    # Note: you shouldn't be using a while loop here.
    # Remember you should be using recursion so your function should
    # call linked_list_reverse_print at some stage!
    # Hint: make sure you aren't calling linked_list_print!
    # ---start student section---
    if list_node is not None:
        linked_list_reverse_print(list_node.next_node)
        print(list_node.item)
    # ===end student section===


def is_in_linked_list(list_node, item):
    """
    Returns True if item is in list, otherwise False.

    >>> first_node = None
    >>> print(is_in_linked_list(first_node,2))
    False
    >>> first_node = Node(1)
    >>> print(is_in_linked_list(first_node,2))
    False
    >>> add_item_to_list(first_node, 2)
    >>> print(is_in_linked_list(first_node,2))
    True
    >>> add_item_to_list(first_node, 3)
    >>> add_item_to_list(first_node, 4)
    >>> add_item_to_list(first_node, 5)
    >>> print(is_in_linked_list(first_node,2))
    True
    >>> is_in_linked_list(first_node,10)
    False
    """
    # Note: you shouldn't be using a while loop here.
    # An item is in the list if it is in the list_node or in the rest of the list
    # The base case is when list_node is None (what should you return in this case?).
    # Remember you should be using recursion so your function should
    # call is_in_linked_list at some stage!
    # ---start student section---
    if list_node is None:
        return False
    if list_node.item == item:
        return True
    return is_in_linked_list(list_node.next_node, item)
    # ===end student section===


# -------------- Recursion with Python lists and strings -----------------
def recursive_string_print(s):
    """
    Prints a string out, one character per line, using recursion
    Think about why this is very inefficient for long strings!
    Remember, you can use slicing and indexing with strings in much the same way
    as you can with list. In the case of strings the first character is at index 0,
    the second character at index 1, etc...
    For example:
    s = 'peach'
    s[0]     # is 'p'
    s[1:3]   # is 'ea'
    s[3:]    # is 'ch'
    s[-1]    # is 'h'
    s[1:]    # is 'each'

    >>> recursive_string_print('blah')
    b
    l
    a
    h
    >>> recursive_string_print('pi')
    p
    i
    """
    # ---start student section---
    if len(s) == 0:
        return
    print(s[0])
    recursive_string_print(s[1:])
    # ===end student section===


def recursive_reverse_string_print(s):
    """
    Prints a string out in reverse, one character per line, using recursion
    Feel free to use list slicing - but do think about why this is very
    inefficient for long strings!
    Remember, you can use slicing and indexing with strings in much the same way
    as you can with list. In the case of strings the first character is at index 0,
    the second character at index 1, etc...
    For example:
    s = 'peach'
    s[0]     # is 'p'
    s[1:3]   # is 'ea'
    s[3:]    # is 'ch'
    s[-1]    # is 'h'
    s[1:]    # is 'each'
    >>> recursive_reverse_string_print('blah')
    h
    a
    l
    b
    >>> recursive_reverse_string_print('pi')
    i
    p
    """
    # ---start student section---
    if len(s) == 0:
        return
    recursive_reverse_string_print(s[1:])
    print(s[0])
    # ===end student section===


def squares(data):
    """A recursive function that takes a list of ints
    and returns a list with the squares of those values.
    The function shouldn't change the original data list.
    Feel free to use list slicing here.
    You shouldn't use list comprehensions, as it would
    effectively be reverting to simple iteration
    >>> print(squares([]))
    []
    >>> print(squares([2]))
    [4]
    >>> squares([1,2,3,4,5])
    [1, 4, 9, 16, 25]
    >>> print(squares([10,20,30,40]))
    [100, 400, 900, 1600]
    >>> print(squares([-11]))
    [121]
    >>> data = list(range(1,11))
    >>> print(squares(data))
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    >>> data
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    # ---start student section---
    if len(data) == 0:
        return []
    else:
        return [data[0] * data[0]] + squares(data[1:])
    # ===end student section===


def total(data):
    """Returns the sum of the values in the data list.
    >>> total([])
    0
    >>> total([1])
    1
    >>> total([1, 2])
    3
    >>> total([1, 2, 3])
    6
    >>> total([1, 2, 3, 4, 5])
    15
    >>> nice_total(list(range(700)))
    244650
    """
    if len(data) == 0:
        return 0
    else:
        return data[0] + total(data[1:])


def nice_total(data, start=0):
    """This example will help you with the following exercises.
        Returns the sum of the values in the data list starting
        from the given start index.
    >>> nice_total([])
    0
    >>> nice_total([1])
    1
    >>> nice_total([1, 2])
    3
    >>> nice_total([1, 2, 3])
    6
    >>> nice_total([1, 2, 3, 4, 5])
    15
    >>> nice_total([1, 2, 3, 4, 5], 3)
    9
    >>> nice_total(list(range(700)))
    244650
    """
    if len(data) <= start:
        return 0
    else:
        return data[start] + nice_total(data, start + 1)


def nice_recursive_string_print(string, index=0):
    """
    Prints a string out, one character per line, staring at index.
    Does so without having to make substring copies, ie, no string slicing.
    By string slicing we mean expressions such as string[1:]
    This means your function will only use list indexing.
    >>> nice_recursive_string_print('blah')
    b
    l
    a
    h
    >>> nice_recursive_string_print('pi')
    p
    i
    >>> nice_recursive_string_print('zippy', 2)
    p
    p
    y
    """
    # ---start student section---
    if index < len(string):
        print(string[index])
        nice_recursive_string_print(string, index + 1)
    # ===end student section===


# ------------------- Just in case you were missing Herbert --------------


def num_rushes(slope_height, rush_height_gain, back_sliding, start_height=0):
    """You may have solved this problem with while loops in COSC121/131.
    This time you'll need to come up with a recursive solution.
    Herbert the Heffalump is trying to climb up a scree slope. He finds that the
    best approach is to rush up the slope until he's exhausted, then pause to
    get his breath back. However, while he pauses each time, the slope settles
    underneath him, carrying him back down part of the slope he just climbed.
    This function calculates how many rushes it takes Herbert to climb up a
    slope of height slope_height metres, given that each rush gains him
    rush_height_gain metres before he slides back back_sliding metres during the
    pause before the next rush. If the start_height is at or above the slope
    height then Herbert has made it, and doesn't need to rush. If a rush gets
    him to the slope height or higher then Herbert won't back slide. The final
    rush will still be counted as one rush, even though it may be of shorter
    duration than the previous rushes. This implementation of num_rushes must
    be written without any loops, import statements, or list comprehensions.
    >>> num_rushes(10, 10, 9)
    1
    >>> print(num_rushes(10, 10, 9, 10))
    0
    >>> print(num_rushes(10, 10, 9, 11))
    0
    >>> print(num_rushes(100, 10, 0, 0))
    10
    >>> print(num_rushes(10, 5, 1, 8))
    1
    >>> print(num_rushes(15, 10, 5))
    2
    >>> print(num_rushes(100, 15, 7))
    12
    >>> print(num_rushes(200, 16, 9))
    28
    """
    if start_height >= slope_height:
        return 0

    # Calculate new height after one rush
    new_height = start_height + rush_height_gain

    # If Herbert reaches or exceeds the slope height after this rush, count this as one rush
    if new_height >= slope_height:
        return 1

    # Otherwise, slide back and continue recursively
    return 1 + num_rushes(
        slope_height, rush_height_gain, back_sliding, new_height - back_sliding
    )


if __name__ == "__main__":
    # These imports are here to save you stress when submitting functions
    # to the quiz server. Normally they would go at the start of the module.
    import doctest
    import os

    os.environ["TERM"] = "linux"  # Suppress ^[[?1034h

    # Comment out the next line if you want to run individual tests
    # doctest.testmod()

    # then uncomment individual doctest runs below
    # doctest.run_docstring_examples(slow_power, None)
    # doctest.run_docstring_examples(quick_power, None)
    # doctest.run_docstring_examples(factorial, None)

    # doctest.run_docstring_examples(linked_list_length, None)
    # doctest.run_docstring_examples(linked_list_print, None)
    # doctest.run_docstring_examples(linked_list_reverse_print, None)
    # doctest.run_docstring_examples(is_in_linked_list, None)

    # doctest.run_docstring_examples(recursive_string_print, None)
    doctest.run_docstring_examples(recursive_reverse_string_print, None)
    doctest.run_docstring_examples(squares, None)
    # doctest.run_docstring_examples(total, None)

    doctest.run_docstring_examples(nice_recursive_string_print, None)
    # doctest.run_docstring_examples(nice_total, None)
    doctest.run_docstring_examples(num_rushes, None)

    # Some other interesting tests to run:
    # -----------------------------------
    # n = 5000
    # print('fib({0:d}) = {1:d}'.format(n, fib_iterative(n)))
    # print('\n')

    # n = 100
    # print('fib({0:d}) = {1:d}'.format(n, fib_iterative(n)))
    # print('\n')

    # n = 31
    # print('fib({0:d}) = {1:d}'.format(n, fib_recursive(n)))
    # print('\n')

    # Given the value for fib_iterative(100) would it be wise
    # to try to run fib_recursive(100)????

    # my_list = Node('b')
    # add_item_to_list(my_list, 'a')
    # linked_list_print(my_list)
