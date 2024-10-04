"""Module for finding test results of quarantined people using a BST."""

import sys
from classes2 import Name, BstNode, bst_nested_repr

# ---------------------------------------------------------------
# NOTE: You might want to import other things here for testing,
# but your submission should only include the import lines above.
# ---------------------------------------------------------------

sys.setrecursionlimit(1024)
WIDTH_FACTOR = 1


def bst_store_pair(root, key, value):
    """
    Stores the key, value pair in the BST tree that starts at the given root.
    This function updates an existing tree so:
      - the root must be an existing BstNode.
      - if root is None an exception is raised.
    Returns the number of key comparisons used.
    Assumes the key is unlikely to already be in the tree and shouldn't check
    for the key being in the current node first, similar to the binary search from assignment 1.
    If the key already exists, the value in that node should be updated
    to the given value. This means that keys in the BST will be unique.
    NOTE: You shouldn't use recursion here as it will eventually cause
    Python to blow up when testing large, worst-case data sets.
    """
    comparisons = 0
    if root is None:
        raise ValueError("I need to have something to add to!")
    current = root
    while current is not None:
        comparisons += 1
        if key < current.key:
            if current.left is None:
                current.left = BstNode(key, value)
                break
            current = current.left
        elif key > current.key:
            if current.right is None:
                current.right = BstNode(key, value)
                break
            current = current.right
        else:
            current.value = value
            break
    return comparisons


def get_value_from_tree(root, key):
    """Returns the value associated with the given key, or None if the key is not present in the tree.
    Your search should only check that the root contains the key
    after ruling out that the key can't be in a sub-tree.
    The tests expect a specific comparison to be first; you will
    need to figure out which one it is :)
    Returns the value/None and the number of key comparisons used.
    NOTE: You shouldn't use recursion here as it will eventually cause
    Python to blow up when testing large, worst-case data sets.
    """
    comparisons = 0
    current = root
    while current is not None:
        comparisons += 1
        if key < current.key:
            current = current.left
        elif key > current.key:
            current = current.right
        else:
            return current.value, comparisons
    return None, comparisons


def min_key_in_bst(root):
    """Returns the minimum key value in the BST starting at root.
    Returns None if root is None.
    Try to do this non-recursively and then try it recursively for fun.
    """
    if root is None:
        return None
    current = root
    while current.left is not None:
        current = current.left
    return current.key


def max_key_in_bst(root):
    """Returns the maximum key value in the BST starting at root.
    Returns None if root is None.
    Try to do this non-recursively and then try it recursively for fun.
    """
    if root is None:
        return None
    current = root
    while current.right is not None:
        current = current.right
    return current.key


def num_nodes_in_tree(root):
    """Returns the number of nodes in the tree starting at root.
    If the root is None, the number of nodes is zero.
    You should use a recursive implementation.
    We will only test with suitably small trees.
    """
    if root is None:
        return 0
    return 1 + num_nodes_in_tree(root.left) + num_nodes_in_tree(root.right)


def bst_depth(root):
    """
    The level of a node is the number of edges from the root to the node.
    The depth is the maximum level of nodes in a tree.
    The depth of a tree starting at the root is:
        - zero if the root is None
        - zero if the root has no children
        - 1 + the max depth of the trees starting at the left and right child
    You should use a recursive implementation.
    We will only test with suitably small trees.
    """
    if root is None:
        return 0
    return 1 + max(bst_depth(root.left), bst_depth(root.right))


def bst_in_order(root, result_list=None):
    """Returns a list containing (key, value) tuples from the BST, in the order of the keys.
    Performs an in-order traversal of the tree, collecting (key, value) pairs as each node is visited.
    Returns an empty list if the root is None.
    This function shouldn't use any key comparisons!
    You should use a recursive implementation.
    We will only test with suitably small trees.
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
    tested contains (nhi, Name, result) tuples for people that have been tested.
    quarantined contains the names of people in quarantine.

    You cannot assume the lists are in any particular order, i.e., you cannot
    assume that either list will be sorted.

    You can assume that there are no duplicate values in either list,
    i.e., within each list any name only appears once.

    The function returns a list and an integer, i.e., results, comparisons.
    The results list contains (name, nhi, result) tuples for each
    name in the quarantined list. If the name isn't in the tested list,
    the nhi and result should be set to None.
    The integer is the number of Name comparisons the function made.

    You must use a BST to store the tested data and
    use the get_value_from_tree function for looking up names
    in the tree. Using name for the key and a (nhi, result) tuple
    for the value makes sense.
    """
    comparisons = 0
    results = []
    bst_root = None
    for nhi, name, result in tested:
        if bst_root is None:
            bst_root = BstNode(name, (nhi, result))
        else:
            comparisons += bst_store_pair(bst_root, name, (nhi, result))
    for name in quarantined:
        value, comp = get_value_from_tree(bst_root, name)
        comparisons += comp
        if value is None:
            results.append((name, None, None))
        else:
            results.append((name, value[0], value[1]))
    return results, comparisons


def smart_bst_result_finder_v1(tested, quarantined):
    """
    Note: this function is an optional bonus exercise
    and isn't worth any marks.

    This function has similar input/output as the
    original bst_result_finder but it utilizes a much
    faster way of building the BST when the tested
    list is fully sorted by name. If the tested list
    is fully sorted by name, then you should write
    an alternative method for adding all the records
    to the BST.

    If the tested list isn't fully sorted by name,
    the old/slow method is still used.
    You should leave the get_value_from_tree function
    the same and use it as before...
    """
    comparisons = 0
    results = []
    if all(tested[i][1] <= tested[i + 1][1] for i in range(len(tested) - 1)):

        def build_balanced_bst(data, start, end):
            if start > end:
                return None
            mid = (start + end) // 2
            node = BstNode(data[mid][1], (data[mid][0], data[mid][2]))
            node.left = build_balanced_bst(data, start, mid - 1)
            node.right = build_balanced_bst(data, mid + 1, end)
            return node

        bst_root = build_balanced_bst(tested, 0, len(tested) - 1)
    else:
        bst_root = None
        for nhi, name, result in tested:
            if bst_root is None:
                bst_root = BstNode(name, (nhi, result))
            else:
                comparisons += bst_store_pair(bst_root, name, (nhi, result))
    for name in quarantined:
        value, comp = get_value_from_tree(bst_root, name)
        comparisons += comp
        if value is None:
            results.append((name, None, None))
        else:
            results.append((name, value[0], value[1]))
    return results, comparisons


def smart_bst_result_finder_v2(tested, quarantined):
    """
    Note: this function is a bonus extra question and
    isn't worth any marks.

    This function has similar input/output as the
    original bst_result_finder but it utilizes a much
    faster way of building the BST when the tested
    list is fully sorted by name.

    If the tested list was sorted and the quarantined list
    is also sorted, then we can speed up the search for values
    in the tree by using an index to the current item in the
    quarantined list and a current pointer to the current
    node in the tested tree. This is a variation of the two
    indices used in the merge part of merge sort or in the
    find common items exercise in Lab 8.
    Doing this means you won't use the normal
    get_value_from_tree function.

    If the tested list isn't fully sorted by name,
    the old method is still used for building the BST
    and for looking up quarantined names in the tree.
    """
    comparisons = 0
    results = []
    if all(tested[i][1] <= tested[i + 1][1] for i in range(len(tested) - 1)) and all(
        quarantined[i] <= quarantined[i + 1] for i in range(len(quarantined) - 1)
    ):
        tested_index = 0
        quarantined_index = 0
        while quarantined_index < len(quarantined):
            while (
                tested_index < len(tested)
                and tested[tested_index][1] < quarantined[quarantined_index]
            ):
                tested_index += 1
                comparisons += 1
            if (
                tested_index < len(tested)
                and tested[tested_index][1] == quarantined[quarantined_index]
            ):
                results.append(
                    (
                        quarantined[quarantined_index],
                        tested[tested_index][0],
                        tested[tested_index][2],
                    )
                )
                tested_index += 1
            else:
                results.append((quarantined[quarantined_index], None, None))
            quarantined_index += 1
    else:
        bst_root = None
        for nhi, name, result in tested:
            if bst_root is None:
                bst_root = BstNode(name, (nhi, result))
            else:
                comparisons += bst_store_pair(bst_root, name, (nhi, result))
        for name in quarantined:
            value, comp = get_value_from_tree(bst_root, name)
            comparisons += comp
            if value is None:
                results.append((name, None, None))
            else:
                results.append((name, value[0], value[1]))
    return results, comparisons


if __name__ == "__main__":
    # Put your own simple tests here.
    # You don't need to submit this code.
    print("Add some tests here...")
