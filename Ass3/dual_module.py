"""Module for finding test results of quarantined people using dual indices."""
from classes3 import Name

# note you might want to import other things here for testing
# but your submission should only include the import line above.



def dual_result_finder(tested, quarantined):
    """This function takes two lists as input.
    tested contains (nhi, Name, result) tuples for people that have been tested
    quarantined contains the names of people in quarantine

    You can assume that lists are sorted in ascending order by Name, that is,
    both lists are already sorted alphabetically/lexigographically.
    You can also assume that there are no duplicate values in either list,
    ie, within each list any name only appears once.

    The function returns a list and an integer, ie, results, comparisons.
    The results list contains (name, nhi, result) tuples for each
    name in the quarantined list. If the name isn't in the tested list
    then the nhi and result should be set to None.
    The integer is the number of Name comparisons the function made.

    Note: this function should use a dual index method that is similar
    to that used in the merge part of a merge sort.
    There are a few ways you can organise the comparisons and you will
    need to figure out the way that passes all the test cases...
    No variation will be better for all data sets, we are just making
    you think a bit harder.
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
    print("Add some tests here...")
