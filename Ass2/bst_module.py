"""Module for finding test results of quarantined people using a BST."""
import sys
from classes2 import Name, BstNode, bst_nested_repr

# IMPORTANT
# To install graphviz for python you will probably first need
# to install graphviz on you system
# = See https://www.graphviz.org/download/ for install instructions
# = Once you have graphviz installed you can run the provided install
# script for installing the graphviz module in Python...
# Then you can uncomment the following line to import it here

# import graphviz as gv

# If you have trouble with graphiz then comment out the import
# and comment out the width, draw_tree_in_graph and draw_tree
# functions in the code below. You don't need to draw anything
# it's just a nice extra.

# ---------------------------------------------------------------
# NOTE: you might want to import other things here for testing
# but your submission should only include the import lines above.
# ---------------------------------------------------------------

# note you might want to import other things here for testing
# but your submission should only include the import lines above.

sys.setrecursionlimit(10**6)
WIDTH_FACTOR = 1

# ----------------------------- graphviz stuff ---------------------------------
# If you want to try drawing some trees using graphviz then uncomment the
# following three function defintions and the import graphviz line, above.
# Remember to install graphviz on your OS and the python graphviz module first
# See the install_graphviz_for_python.py module for details
# NOTE: You shouldn't include any code that calls graphviz in quiz submissions.


# def width(root):
# """ Returns the width of a tree scaled by the WIDTH_FACTOR """
# if root is None:
# return 0
# left_width = width(root.left)
# right_width = width(root.right)
# whole_width = WIDTH_FACTOR + left_width + right_width
# return whole_width


# def draw_tree_in_graph(root, graph, level=0, left_x=0, parent=None):
# """
# Adds the nodes and edges for the tree to the graphviz graph.
# You won't typically call this directly, it is called the draw_tree.
# """
# if root is None:
# return   # do nothing
# left_width = width(root.left)
# current_pos = left_x + left_width + WIDTH_FACTOR
# this_name = str(root.key)
# graph.node(this_name, pos=f'{current_pos}, {-level}!', label=this_name)
# if parent is not None:
# parent_name = str(parent.key)
# graph.edge(parent_name, this_name)
# draw_tree_in_graph(root.left, graph,
# level=level+1,
# left_x=left_x,
# parent=root)
# draw_tree_in_graph(root.right, graph,
# level=level+1,
# left_x=current_pos,
# parent=root)


# def draw_tree(root, filename='_a_tree'):
# """ Draws the tree, starting at the given BST tree root node.
# You can call this function after building a tree, eg, in bst_result_finder.
# Of course you will only want to draw small trees (with <=50 nodes or so).
# Please take any calls to this function out before submitting code.
# """
## change format to pdf if you want to draw big trees :)
# graph = gv.Digraph(engine='neato', format='png')
# graph.attr('graph', bgcolor='transparent')
# graph.attr('node',
# shape='rectangle',
# fillcolor='white',
# style='filled',
# fontsize='12pt')
# draw_tree_in_graph(root, graph)
# graph.render(filename, view=True)

# ----------------------------- end of graphviz stuff --------------------------


def bst_store_pair(root, key, value):
    """
    Stores the key, value pair in the BST tree that starts at the given root.
    This function updates an existing tree so:
      - the root must be an existing BstNode.
      - if root is None an exception is raised.
    Returns the number of key comparisons used.
    Assumes the key is unlikely to already be in the tree and shouldn't check
    for the key being in the current node first, in a similar fashion to the
    binary search from assignment 1. You must figure out which key comparison
    is done first. The simple BST tests will help you figure it out.
    If the key already exists then the value in that node should be updated
    to the given value. This means that keys in the bst will be unique.
    NOTE: You shouldn't use recursion here as it will eventually cause
    Python to blow-up when testing large, worst case, data sets.
    """
    comparisons = 0
    if root is None:
        raise ValueError("I need to have something to add to!")

    current = root
    while True:
        # First comparison: key < current.key
        comparisons += 1
        if key < current.key:
            if current.left is None:
                current.left = BstNode(key, value)
                break
            current = current.left
            continue

        # Second comparison: key > current.key
        comparisons += 1
        if key > current.key:
            if current.right is None:
                current.right = BstNode(key, value)
                break
            current = current.right
            continue

        current.value = value
        break

    return comparisons


def get_value_from_tree(root, key):
    """Returns the value associated with the given key,
    or None if the key is not present in the tree.
    Your search should only check that the root contains the key
    after ruling out that the key can't be in a sub tree.
    That is check if you need to search one of the sub trees first.
    The tests expect a specific comparison to be first, you will
    need to figure out which one it is :)
    Returns the value/None and the number of key comparisons used.
    NOTE: You shouldn't use recursion here as it will eventually cause
    Python to blow-up when testing large, worst case, data sets.
    """
    comparisons = 0
    value = None
    while root is not None:
        comparisons += 1
        if key < root.key:
            root = root.left
            continue
        comparisons += 1
        if key > root.key:
            root = root.right
            continue
        else:
            value = root.value
            break
    return value, comparisons


def min_key_in_bst(root):
    """ Returns the minimum key value in the bst starting at root.
    Returns None if root is None
    Try to do this non-recursively and then try it recursively for fun.
    """
    result = None
    if root is not None:
        while root.left is not None:
            root = root.left
        result = root.key
    return result


def max_key_in_bst(root):
    """ Returns the maximum key value in the bst starting at root.
    Returns None if root is None.
    Try to do this non-recursively and then try it recursively for fun.
    """
    result = None
    if root is not None:
        while root.right is not None:
            root = root.right
        result = root.key
    return result


def num_nodes_in_tree(root):
    """ Returns the number of nodes in the tree starting at root.
    If the root is None then the number of nodes is zero.
    """
    num_nodes = 0
    if root is not None:
        num_nodes = 1 + num_nodes_in_tree(root.left) + num_nodes_in_tree(root.right)
    return num_nodes


def bst_depth(root):
    """ The level of a node is the number of edges from the root to the node
        The depth is the maximum level of nodes in a tree.
        Remember, the level of a node is how many edges there are on a path
        from the root to the node.
        So, the depth of a tree starting at the root is:
        - zero if the root is None
        - zero if the root has no children
        - 1 + the max depth of the trees starting at the left and right child
    """
    depth = -1
    if root is not None:
        depth = 1 + max(bst_depth(root.left), bst_depth(root.right))
    return depth


def bst_in_order(root, result_list=None):
    """ Returns a list containing (key, value) tuples
    from the bst, in the order of the keys.
    Basically does an in order traversal of the tree
    collecting (key, value) pairs as each node is visited.
    Returns an empty list if the root is None.
    This function shouldn't use any key comparisons!
    """
    if result_list is None:
        result_list = []
    if root is not None:
        bst_in_order(root.left, result_list)
        result_list.append((root.key, root.value))
        bst_in_order(root.right, result_list)
    return result_list


def bst_result_finder(tested, quarantined):
    """This function takes two lists as input.
    tested contains (nhi, Name, result) tuples for people that have been tested
    quarantined contains the names of people in quarantine

    You cannot assume the lists are in any particular order, ie, you cannot
    assume that either list will be sorted.

    You can assume that there are no duplicate values in either list,
    ie, within each list any name only appears once.

    The function returns a list and an integer, ie, results, comparisons.
    The results list contains (name, nhi, result) tuples for each
    name in the quarantined list. If the name isn't in the tested list
    then the nhi and result should be set to None.
    The integer is the number of Name comparisons the function made.

    You must use a BST to store the tested data and
    use the get_value_from_tree function for looking up names
    in the tree. Using name for the key and a (nhi, result) tuple
    for the value makes sense.

    """
    comparisons = 0
    results = []
    root = BstNode(tested[0][1], (tested[0][0], tested[0][2]))
    for nhi, name, result in tested[1:]:
        comparisons += bst_store_pair(root, name, (nhi, result))
    for name in quarantined:
        result, comps = get_value_from_tree(root, name)
        comparisons += comps
        if result is None:
            results.append((name, None, None))
        else:
            results.append((name, result[0], result[1]))
    return results, comparisons

def get_list_in_middle_order(list, root):
    """ Similiar to binary search and should make the tree even"""
    if len(list) == 0:
        return None
    middle_val = len(list) // 2
    if root is None:
        comp = 0
        root = BstNode(list[middle_val][1], (list[middle_val][0], list[middle_val][2]))
    else:
        comp = bst_store_pair(root, list[middle_val][1], (list[middle_val][0], list[middle_val][2]))
    get_list_in_middle_order(list[:middle_val], root)
    get_list_in_middle_order(list[middle_val+1:], root)
    return root, comp



def smart_bst_result_finder_v1(tested, quarantined):
    """
    Note: this function is an optional bonus exercise
    and isn't worth any marks.

    This function has similar input/output as the
    original bst_result_finder but it utilises a much
    faster way of building the bst when the tested
    list is fully sorted by name. If the tested list
    is fully sorted by name then you should write
    an alternative method for adding all the records
    to the bst.

    If the tested list isn't fully sorted by name then
    the old/slow method is still used.
    You should leave the get_value_from_tree function
    the same, and use it as before...
    """
    comparisons = 0
    results = []
    # ---start student section---
    # ===end student section===
    return results, comparisons


def smart_bst_result_finder_v2(tested, quarantined):
    """
    Note: this function is a bonus extra question and
    isn't worth any marks.

    This function has similar input/output as the
    original bst_result_finder but it utilises a much
    faster way of building the bst when the tested
    list is fully sorted by name.

    If the tested list was sorted and the quarantined list
    is also sorted then we can speed up the looking for values
    in the tree by using an index to the current item in the
    quarantined list and a current pointer to the current
    node in the tested tree. This is a variation of the two
    indices that are used in the merge part of merger sort
    or in the find common items exercise in Lab 8   .
    Doing this means you won't use the normal
    get_value_from_tree function.

    If the tested list isn't fully sorted by name then
    the old method is still used for building the bst
    and for looking up quarantined names in the tree.

    """
    comparisons = 0
    results = []
    # ---start student section---
    pass
    # ===end student section===
    return results, comparisons


if __name__ == '__main__':
    # put your own simple tests here
    # you don't need to submit this code
    print("Testing bst_store_pair")
