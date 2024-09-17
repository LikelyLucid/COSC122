import doctest
import os

# --------------------------------------------------------------------------


def load_file(file_name):
    """ The file should contain one integer value per line.
    A list of integers is returned.
    """
    nums = [
        int(line)
        for line in open(file_name, encoding='utf-8').read().splitlines()]
    return nums


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
class Node(object):

    """Represents a node in a binary tree."""

    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        val = repr(self.value)
        left = repr(self.left)
        right = repr(self.right)
        return f'[{val}, l:{left}, r:{right}]'


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


class BinarySearchTree(object):

    """Implements the operations for a Binary Search Tree."""
    # -------------------------------------------

    def __init__(self):
        self.root = None

    # -------------------------------------------
    def insert(self, value):
        """
        Inserts a new item into the tree.

        >>> b = BinarySearchTree()
        >>> b.insert(5)
        >>> b.insert(3)
        >>> b.root.left.value
        3
        >>> b.insert(4)
        >>> repr(b.root.left.right.value)
        '4'
        """
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    # -------------------------------------------
    def _insert(self, subtree_root, value):
        """
        Recursively locates the correct position in the subtree starting
        at 'subtree_root' to insert the given 'value',
        and attaches a Node containing the 'value' to the tree.
        NOTE: _ before a method name indicates that it is a private method and
        should only be called by other methods within the class.
        Most of these private methods are recursive in this class.
        """
        if value < subtree_root.value:
            # Insert to the left
            if subtree_root.left is None:
                subtree_root.left = Node(value)
            else:
                self._insert(subtree_root.left, value)
        else:
            # Insert to the right
            if subtree_root.right is None:
                subtree_root.right = Node(value)
            else:
                self._insert(subtree_root.right, value)

    # -------------------------------------------
    def in_order_items(self):
        """
        Returns a sorted list of all items in the tree using in-order traversal.

        >>> b = BinarySearchTree()
        >>> b.insert(5)
        >>> b.insert(3)
        >>> b.insert(4)
        >>> b.in_order_items()
        [3, 4, 5]
        >>> b.insert(7)
        >>> b.in_order_items()
        [3, 4, 5, 7]
        """
        out_list = []
        # out_list will be built up as we recurse through the tree
        # out_list is change in-place so no answer is returned from _in_order_items
        self._in_order_items(self.root, out_list)
        return out_list

    # -------------------------------------------
    def _in_order_items(self, subtree_root, out_list):
        """Performs a in-order traversal of the subtree with the
        given subtree_root, adding values from visited nodes to
        out_list. Note: out_list is mutable and updated in-place so
        no answer is returned.
        """
        # ---start student section---
        pass
        # ===end student section===

    # -------------------------------------------
    def pre_order_items(self):
        """
        Returns a list of all items in the tree using pre-order traversal.

        >>> b = BinarySearchTree()
        >>> b.insert(5)
        >>> b.insert(3)
        >>> b.insert(4)
        >>> b.pre_order_items()
        [5, 3, 4]
        """
        out_list = []
        # out_list will be built up as we recurse through the tree
        # out_list is change in-place so no answer is returned from _pre_order_items
        self._pre_order_items(self.root, out_list)
        return out_list

    # -------------------------------------------
    def _pre_order_items(self, subtree_root, out_list):
        """Performs a pre-order traversal of the subtree with the
        given subtree_root, adding values from visited nodes to
        out_list. Note: out_list is mutable and updated in-place so
        no answer is returned.
        """
        # ---start student section---
        pass
        # ===end student section===

    # -------------------------------------------
    def post_order_items(self):
        """
        Returns a list of all items in the tree using post-order traversal.

        >>> b = BinarySearchTree()
        >>> b.insert(5)
        >>> b.insert(3)
        >>> b.insert(4)
        >>> b.post_order_items()
        [4, 3, 5]
        """
        out_list = []
        self._post_order_items(self.root, out_list)
        return out_list

    # -------------------------------------------
    def _post_order_items(self, subtree_root, out_list):
        """Performs a post-order traversal from subtree_root,
        adding the values from each node visited to 'out_list'."""
        # ---start student section---
        pass
        # ===end student section===

    # -------------------------------------------
    def __contains__(self, value):
        """
        Returns True if the tree contains an item, False otherwise.

        >>> b = BinarySearchTree()
        >>> b.insert(5)
        >>> b.insert(3)
        >>> b.insert(4)
        >>> 4 in b
        True
        >>> 999 in b
        False
        """
        return self._contains(self.root, value)

    # -------------------------------------------
    def _contains(self, subtree_root, value):
        # Base case -- reached the end of the subtree_root
        if subtree_root is None:
            return False
        # Found the item
        if value == subtree_root.value:
            return True
        # The item is to the left
        elif value < subtree_root.value:
            return self._contains(subtree_root.left, value)
        # The item is to the right
        else:
            return self._contains(subtree_root.right, value)

    # -------------------------------------------
    def __len__(self):
        """
        Returns the number of nodes in the tree.

        >>> b = BinarySearchTree()
        >>> b.insert(5)
        >>> b.insert(3)
        >>> len(b)
        2
        >>> b.insert(4)
        >>> len(b)
        3
        """
        return self._len(self.root)

    # -------------------------------------------
    def _len(self, subtree_root):
        if subtree_root is None:
            return 0
        return 1 + self._len(subtree_root.left) + self._len(subtree_root.right)

    # -------------------------------------------
    def remove(self, value):
        """
        Removes the first occurrence of value from the tree.

        >>> b = BinarySearchTree()
        >>> b.insert(5)
        >>> b.insert(3)
        >>> b.insert(4)
        >>> 4 in b
        True
        >>> b.remove(3)
        >>> 3 in b
        False
        >>> b.insert(9)
        >>> b.insert(7)
        >>> b.insert(6)
        >>> b.insert(6.5)
        >>> b.remove(5)
        >>> b.root.value
        6
        >>> 6.5 in b
        True
        """
        self.root = self._remove(self.root, value)

    def _remove(self, subtree_root, value):
        """ NOTE: You don't need to write anything in this method.
        You do need to understand it though :)
        """
        # value is not in the tree
        if subtree_root is None:
            return subtree_root
        # The item should be on the left
        if value < subtree_root.value:
            subtree_root.left = self._remove(subtree_root.left, value)
        # The item should be on the right
        elif value > subtree_root.value:
            subtree_root.right = self._remove(subtree_root.right, value)
        # The item to be deleted IS subtree_root!
        else:
            if subtree_root.left is None and subtree_root.right is None:
                # No children.
                subtree_root = None
            elif subtree_root.left is not None and subtree_root.right is None:
                # One left child.
                subtree_root = subtree_root.left
            elif subtree_root.left is None and subtree_root.right is not None:
                # One right child.
                subtree_root = subtree_root.right
            else:
                # Two children.
                # subtree_root will be unchanged in this case
                # its value will be changed to the value
                # of the in order successor
                subtree_root.value = self._pop_in_order_successor(subtree_root)
        return subtree_root

    # -------------------------------------------
    def _pop_in_order_successor(self, subtree_root):
        """
        Returns the value of the in-order successor and removes it from the tree.
        The in order successor will be the smallest value in the right subtree.
        Note: this function will be called when the node to remove has two children
        If the right child has no left child this is easy otherwise it needs
        to use the _recursive_pop_min function ...

        NOTE: You don't need to write anything in this method either :)

        >>> b = BinarySearchTree()
        >>> b.insert(7)
        >>> b.insert(5)
        >>> b.insert(15)
        >>> b.insert(9)
        >>> b.insert(13)
        >>> b.insert(11)

        >>> b._pop_in_order_successor(b.root)
        9
        >>> repr(b.root.right)
        '[15, l:[13, l:[11, l:None, r:None], r:None], r:None]'

        >>> b._pop_in_order_successor(b.root)
        11
        >>> repr(b.root.right)
        '[15, l:[13, l:None, r:None], r:None]'

        >>> b._pop_in_order_successor(b.root)
        13
        >>> repr(b.root.right)
        '[15, l:None, r:None]'

        >>> b._pop_in_order_successor(b.root)
        15
        >>> repr(b.root)
        '[7, l:[5, l:None, r:None], r:None]'
        """
        if subtree_root.right.left is None:
            successor_value = subtree_root.right.value
            subtree_root.right = subtree_root.right.right
        else:
            successor_value = self._pop_min_recursive(subtree_root.right)
        return successor_value

    # -------------------------------------------
    def _pop_min_recursive(self, subtree_root):
        """ Recursive code.

        NOTE: Here's where you need to write some code :)

         Returns the min value and removes the node from the subtree.
         If the left child of subtree has no left child,
         then the left child contains the min value,
         so de-link  the left child from the subtree and return its value.
         Remember to keep the left child's right child connected to the subtree.
        """
        # ---start student section---
        pass
        # ===end student section===
        # return min_value

    def __repr__(self):
        return repr(self.root)

    def __str__(self):
        return str(self.root)


if __name__ == '__main__':
    os.environ['TERM'] = 'linux'  # Suppress ^[[?1034h
    doctest.testmod()

