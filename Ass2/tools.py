"""Module for reading test data."""
from classes2 import Name
import random



def make_name_list(iterable, sort_order=None):
    """ Takes an iterable of strings and returns a list of Name objects.
    This is helpful when testing.
    sort_order can be given as 'name', or 'random' with obvious results - see below.
    For example:
    make_name_list(['a', 'b', 'c', 'd') returns a list with [Nameame('a'), Name('b')...]
    make_name_list('abcd') also returns a list with [Name('a'), Name('b')...]
    """
    results= []
    for string in iterable:
        results.append(Name(string))
    if sort_order == 'name':
        results.sort()
    elif sort_order == 'random':
        random.shuffle(results)
    # else leave in the order they were given
    return results



def make_tested_list(iterable, sort_order=None, test_result=True):
    """ Takes an iterable of strings and returns a tested list with (nhi, name, result) tuples.
    The result is the same for all records, ie, equals test_result which is True by default
    The nhi will start at 1 and count up as it goes.
    sort_order can be given as 'name', 'nhi', or 'random' with obvious results - see below.
    This is helpful when testing.
    For example:
    make_tested_list(['a', 'b', 'c', 'd']) returns a list with:
        [(0, Name('a'), True), (1, Name('b'), True), ..., (4, Name('d'), True)]
    make_tested_list('abcd') also returns a list with:
        [(0, Name('a'), True), (1, Name('b'), True), ..., (4, Name('d'), True)]
    """
    results = []
    nhi = 1
    for string in iterable:
        record = (nhi, Name(string), test_result)
        results.append(record)
        nhi += 1
    if sort_order == 'name':
        results.sort(key= lambda x:x[1])
    elif sort_order == 'nhi':
        results.sort(key= lambda x:x[0])
    elif sort_order == 'random':
        random.shuffle(results)
    # else just leave in the order of the supplied iterable
    return results



def read_test_data(filename):
    """Reads a test data file and returns a triple containg the list of tested
    people, the list of quarantined people and the list of results
    for quarantined people.
    The list of tested contains (nhi, Name, result) tuples
    The quarantined list is a list of Names
    The quarantined_results list is a list of (Name, nhi, result) tuples
    """
    tested = []
    quarantined = []
    quarantined_results = []
    with open(filename) as test_data_file:
        #Read details of tested people
        current_line = _get_next_line(test_data_file)
        tested_size = int(current_line)
        for _ in range(tested_size):
            current_line = _get_next_line(test_data_file)
            nhi, name_str, result_str = current_line.split(',')
            result = True if result_str == 'True' else False
            record = (int(nhi), Name(name_str), result)
            tested.append(record)

        #Read quarantined names
        current_line = _get_next_line(test_data_file)
        quarantined_size = int(current_line)
        for _ in range(quarantined_size):
            current_line = _get_next_line(test_data_file)
            quarantined.append(Name(current_line))

        #Read expected details of quarantined people
        for _ in range(quarantined_size):   # will have same number as quarantined
            current_line = _get_next_line(test_data_file)
            #print(current_line)
            name_str, nhi_str, result_str = current_line.split(',')
            if nhi_str == 'None':
                nhi = None
            else:
                nhi = int(nhi_str)
            if result_str == 'True':
                result = True
            elif result_str == 'False':
                result = False
            else:
                result = None
            record = (Name(name_str), nhi, result)
            quarantined_results.append(record)

    return tested, quarantined, quarantined_results



def _get_next_line(test_data_file):
    """Reads and returns one line from a test data file. Returns None if the end
    of file is reached."""
    current_line = test_data_file.readline()
    #Comment lines are not read.
    while current_line.startswith('#'):
        current_line = test_data_file.readline()

    #None is returned if the end of the file is reached.
    if len(current_line) == 0:
        return None
    return current_line.rstrip()

