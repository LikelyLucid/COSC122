""" Binary search is trickier than you think.
Remember your binary search should only use one comparison
per while loop, ie, one comparison per halving.
"""

import tools


def binary_search(tested_list, target_name):
    """Binary serach that made me wanna kms"""
    low = 0
    high = len(tested_list) - 1
    comparisons = 0

    while low < high:
        mid = (low + high) // 2  # Middle index
        name = tested_list[mid][1]  # Name
        comparisons += 1
        if name < target_name:  # If name is less than target_name
            low = mid + 1
        else:  # If name is greater than target_name
            high = mid
    final_name = tested_list[low][1]  # Final name
    comparisons += 1

    if final_name == target_name:  # If final name is equal to target_name
        name = tested_list[low][1]  # Name
        nhi = tested_list[low][0]  # NHI
        result = tested_list[low][2]  # Result
    else:  # If final name is not equal to target_name
        name = target_name
        nhi = None
        result = None
    return (name, nhi, result), comparisons


def binary_result_finder(tested_list, quarantined):
    """The tested list contains (nhi, Name, result) tuples
    and isn't guaranteed to be in any order
    quarantined is a list of Name objects
    and isn't guaranteed to be in any order
    This function should return a list of (Name, nhi, result)
    tuples and the number of comparisons made
    The result list must be in the same order
    as the quarantined list.
    The nhi and result should both be set to None if
    the Name isn't found in tested_list
    You must keep track of all the comparisons
    made between Name objects.
    Your function must not alter the tested_list or
    the quarantined list in any way.
    """
    total_comparisons = 0
    results = []
    for person in quarantined:
        result, comparisons = binary_search(tested_list, person)
        results.append(result)
        total_comparisons += comparisons
    return results, total_comparisons


# Don't submit your code below or pylint will get annoyed :)
if __name__ == "__main__":
    # Example test case
    quarantined = tools.make_name_list(["Bob", "Abba", "Faba"])
    tested = tools.make_tested_list(
        ["Bingle", "Bob", "Arthur", "Faba", "Zabba"], sort_order="name"
    )
    print(quarantined)
    print(tested)
    results, comparisons = binary_result_finder(tested, quarantined)
    print(results, comparisons)
