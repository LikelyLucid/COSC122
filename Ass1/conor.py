import tools

# uncomment the next line if you want to make some Name objects
from classes import Name


def linear_result_finder(tested_list, quarantined):
    """The tested list contains (nhi, Name, result) tuples
    and isn't guaranteed to be in any order
    quarantined is a list of Name objects
    and isn't guaranteed to be in any order
    This function should return a list of (Name, nhi, result)
    tuples and the number of comparisons made
    The result list must be in the same order
    as the  quarantined list.
    The nhi and result should both be set to None if
    the Name isn't found in tested_list
    You must keep track of all the comparisons
    made between Name objects.
    Your function must not alter the tested_list or
    the quarantined list in any way.
    """
    total_comparisons = 0
    results = []
    # ---start student section---
    for name2 in quarantined:
        for tuple in tested_list:
            name1 = tuple[1]
            total_comparisons += 1
            if name1 == name2:
                results.append((tuple[1], tuple[0], tuple[2]))
                break
        else:
            results.append((name2, None, None))

    # ===end student section===
    return results, total_comparisons


# Don't submit your code below or pylint will get annoyed 🙂
if __name__ == "__main__":
    # write your own simple tests here
    # eg
    tested = [
        (1, Name("Lee"), True),
        (12123132, Name("Bob"), True),
        (123, Name("Alice"), False),
        (152563, Name("John"), False),
        (76621, Name("Robert"), True),
    ]
    quarantined = [Name("Bob"), Name("Robert"), Name("Lee")]
    print(linear_result_finder(tested, quarantined))

    tested = []
    quarantined = []
    print(linear_result_finder(tested, quarantined))

    tested = [
        (1, Name("Lee"), True),
        (12123132, Name("Bob"), True),
        (123, Name("Alice"), False),
        (152563, Name("John"), False),
        (76621, Name("Robert"), True),
    ]
    quarantined = []
    print(linear_result_finder(tested, quarantined))
