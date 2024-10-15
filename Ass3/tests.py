"""Module containing the unit tests for the result getting functions."""
import os
import time
import shutil
import tools
import unittest
import math
from classes3 import Name, Node
from dual_module import dual_result_finder
from hash_module import HashTable, hash_result_finder
from stats import IS_MARKING_MODE, NAME_COMPS, HASH_TABLES_CREATED, StatCounter
from tools import read_test_data, make_name_list, make_tested_list


actual_count = StatCounter.get_count
lock_counter = StatCounter.lock_counter
unlock_counter = StatCounter.unlock_counter

DATA_DIR = './test_data/'

# Set the fp;;pwomg to True to get time taken for each test printed. These may all come out
# at the end of testing.
PRINT_TEST_TIMES = False


def intersect_size_from_filename(filename):
    """ Returns the number of people in the quarantined
    list that have results in the tested list.
    Basically the size of the intersction of names
    between the two lists.
    eg
    ig filename is 'test_data-20i-10r-5-a.txt'
    then this function would return 5
    """
    bits = filename.split('-')
    return int(bits[3])


def tested_size_from_filename(filename):
    """ Returns the number of people in the tested list
    eg
    ig filename is 'test_data-20i-10r-5-a.txt'
    then this function would return 20
    """
    bits = filename.split('-')
    raw = bits[1].strip('in')
    return int(raw)


class BaseTester(unittest.TestCase):

    def setUp(self):
        """This runs before each test case"""
        unlock_counter(NAME_COMPS)
        unlock_counter(HASH_TABLES_CREATED)
        StatCounter.reset_counts()
        self.start_time = time.perf_counter()
        # self.function_to_test should be setup by subclasses with the student function
        # that they want to test

    def tearDown(self):
        self.end_time = time.perf_counter()
        test_time = self.end_time - self.start_time
        if PRINT_TEST_TIMES:
            print(f"{test_time:.4f}s", end=" ")


    def AssertListsEqual(self, list1, list2):
        """ Locks the counter when comparing lists """
        lock_counter(NAME_COMPS)
        self.assertEqual(list1, list2)
        unlock_counter(NAME_COMPS)



class BaseTests(BaseTester):

    def get_bounds(self, left_length, right_length):
        raise NotImplementedError("This method should be "
                                  "implemented by a subclass.")

    def result_list_test(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined)
        self.AssertListsEqual(results, expected_results)
        self.assertEqual(type(results), type(expected_results))

    def comparisons_test(self, test_filename, expected_comparisons):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined)
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but was expected to use {expected_comparisons}."
        self.assertEqual(comparisons, expected_comparisons, msg=message)

    def internal_comparisons_test(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined)
        actual_comparisons = actual_count(NAME_COMPS)
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but it actually used {actual_comparisons}. "
        message += "This means you are miscounting Name comparisons, eg, "
        message += "not counting Name comparisons when they are made or "
        message += "counting Name comparisons that weren't made."
        self.assertEqual(comparisons, actual_comparisons, msg=message)

    def comparisons_within_bound_test(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined)
        intersect_size = intersect_size_from_filename(test_filename)
        lower_bound, upper_bound = self.get_bounds(len(tested),
                                                   len(quarantined),
                                                   intersect_size)
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but was expected to use at least {lower_bound}."
        self.assertGreaterEqual(comparisons, lower_bound, msg=message)
        message2 = f"Your code reported using {comparisons} Name comparisons "
        message2 += f"but was expected to use no more than {upper_bound}."
        self.assertLessEqual(comparisons, upper_bound, msg=message2)


    def exact_comparisons_test(self, test_filename, expected_comparisons):
        # checks vs an exact number of comparisons
        # as opposed to a range
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined)
        intersect_size = intersect_size_from_filename(test_filename)
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but was expected to use {expected_comparisons}."
        self.assertEqual(comparisons, expected_comparisons, msg=message)





class TrivialListTest(BaseTests):

    def setUp(self):
        super().setUp()

    def test_single_result_small(self):
        filename = 'test_data-10n-10n-1-a.txt'
        self.result_list_test(filename)


class SmallTests(BaseTests):

    def setUp(self):
        super().setUp()

    def test_no_results_small(self):
        filename = 'test_data-10n-10n-0-a.txt'
        self.result_list_test(filename)

    def test_single_results_small(self):
        filename = 'test_data-10n-10n-1-a.txt'
        self.result_list_test(filename)

    def test_10_results_small(self):
        filename = 'test_data-10n-10n-10-a.txt'
        self.result_list_test(filename)

    def test_no_results_small_comparisons_within_bound(self):
        filename = 'test_data-10n-10n-0-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_single_results_small_comparisons_within_bound(self):
        filename = 'test_data-10n-10n-1-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_10_results_small_comparisons_within_bound(self):
        filename = 'test_data-10n-10n-10-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_no_results_small_internal_comparisons(self):
        filename = 'test_data-10n-10n-0-a.txt'
        self.internal_comparisons_test(filename)

    def test_single_results_small_internal_comparisons(self):
        filename = 'test_data-10n-10n-1-a.txt'
        self.internal_comparisons_test(filename)

    def test_10_results_small_internal_comparisons(self):
        filename = 'test_data-10n-10n-10-a.txt'
        self.internal_comparisons_test(filename)


class MediumTests(BaseTests):

    def setUp(self):
        super().setUp()

    def test_no_results_medium(self):
        filename = 'test_data-50n-50n-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_medium_comparisons_within_bound(self):
        filename = 'test_data-50n-50n-0-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_no_results_medium_internal_comparisons(self):
        filename = 'test_data-50n-50n-0-a.txt'
        self.internal_comparisons_test(filename)

    def test_single_results_medium(self):
        filename = 'test_data-50n-50n-1-a.txt'
        self.result_list_test(filename)

    def test_single_results_medium_comparisons_within_bound(self):
        filename = 'test_data-50n-50n-1-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_single_results_medium_internal_comparisons(self):
        filename = 'test_data-50n-50n-1-a.txt'
        self.internal_comparisons_test(filename)

    def test_10_results_medium(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_medium_comparisons_within_bound(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_10_results_medium_internal_comparisons(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.internal_comparisons_test(filename)


class BigTests(BaseTests):

    def setUp(self):
        super().setUp()

    def test_no_results_big(self):
        filename = 'test_data-1000n-1000n-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_big_comparisons_within_bound(self):
        filename = 'test_data-1000n-1000n-0-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_single_results_big(self):
        filename = 'test_data-1000n-1000n-1-a.txt'
        self.result_list_test(filename)

    def test_single_results_big_comparisons_within_bound(self):
        filename = 'test_data-1000n-1000n-1-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_single_results_big_internal_comparisons(self):
        filename = 'test_data-1000n-1000n-1-a.txt'
        self.internal_comparisons_test(filename)

    def test_10_results_big(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_big_comparisons_within_bound(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_10_results_big_internal_comparisons(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.internal_comparisons_test(filename)


class HugeTests(BaseTests):

    def setUp(self):
        super().setUp()

    def test_no_results_huge(self):
        filename = 'test_data-10000n-10000n-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_huge_comparisons_within_bound(self):
        filename = 'test_data-10000n-10000n-0-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_single_results_huge(self):
        filename = 'test_data-10000n-10000n-1-a.txt'
        self.result_list_test(filename)

    def test_single_results_huge_comparisons_within_bound(self):
        filename = 'test_data-10000n-10000n-1-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_single_results_huge_internal_comparisons(self):
        filename = 'test_data-10000n-10000n-1-a.txt'
        self.internal_comparisons_test(filename)

    def test_10_results_huge_comparisons_within_bound(self):
        filename = 'test_data-10000n-10000n-10-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_10_results_huge(self):
        filename = 'test_data-10000n-10000n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_huge_internal_comparisons(self):
        filename = 'test_data-10000n-10000n-10-a.txt'
        self.internal_comparisons_test(filename)



class GinormousTests(BaseTests):

    def setUp(self):
        super().setUp()

    def test_no_results_ginormous(self):
        filename = 'test_data-100000n-10000n-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_ginormous_comparisons_within_bound(self):
        filename = 'test_data-100000n-10000n-0-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_single_results_ginormous(self):
        filename = 'test_data-100000n-10000n-1-a.txt'
        self.result_list_test(filename)

    def test_single_results_ginormous_comparisons_within_bound(self):
        filename = 'test_data-100000n-10000n-1-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_single_results_ginormous_internal_comparisons(self):
        filename = 'test_data-100000n-10000n-1-a.txt'
        self.internal_comparisons_test(filename)

    def test_10_results_ginormous_comparisons_within_bound(self):
        filename = 'test_data-100000n-10000n-10-a.txt'
        self.comparisons_within_bound_test(filename)

    def test_10_results_ginormous(self):
        filename = 'test_data-100000n-10000n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_ginormous_internal_comparisons(self):
        filename = 'test_data-100000n-10000n-10-a.txt'
        self.internal_comparisons_test(filename)






# --------------------  Hash Table tests ---------------------------
# These tests test your hash table class
class TrivialHashTableTests(BaseTester):

    def setUp(self):
        super().setUp()
        Name.reset_hashes()
        HashTable.reset_memory_used()

    def test_add_and_find_one_name(self):
        table = HashTable(11)
        name1 = Name('Tim')
        value1 = (1234, True)
        table.store_pair(name1, value1)
        self.assertTrue(table.get_value(name1), value1)


class HashTableTests(BaseTester):

    def setUp(self):
        super().setUp()
        Name.reset_hashes()
        HashTable.reset_memory_used()

    def test_add_one_name(self):
        # this should work out of the box
        # hopefully you haven't borked it!
        table = HashTable(11)
        name1 = Name('Tim')
        value1 = (1234, True)
        table.store_pair(name1, value1)
        # Tim should be only voter in slot 8
        head = table._data[8]
        self.assertEqual(len(head), 1)
        first_name = head.key
        self.assertEqual(first_name, name1)

    def test_add_two_names(self):
        # this should work out of the box
        # hopefully you haven't borked it!
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        table.store_pair(fee, (1234, True))
        table.store_pair(jo, (5678, False))
        # Fee and Jo should both be in slot 3
        head = table._data[3]
        self.assertEqual(len(head), 2)
        # Jo will be the first name in slot 3
        # as nodes are inserted at the start of
        # the linked list and jo was added
        # after fee
        first_name = head.key
        self.assertEqual(first_name, jo)
        # Fee will be the second name in slot 3
        second_name = head.next_node.key
        self.assertEqual(second_name, fee)

    def test_simple_add_and_find(self):
        table = HashTable(11)
        fee = Name('Fee')
        table.store_pair(fee, (1234, True))
        self.assertEqual(table.get_value(fee), (1234,True))

    def test_add2_and_find_1_v1(self):
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        table.store_pair(fee, (123, True))
        table.store_pair(jo, (567, True))
        self.assertEqual(table.get_value(fee), (123, True))
        # think about why 2 comparisons have been made
        self.assertEqual(table.comparisons_used, 2)

    def test_add2_and_find_1_v2(self):
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        table.store_pair(fee, (123, True))
        table.store_pair(jo, (567, True))
        self.assertEqual(table.get_value(jo), (567, True))
        # think about why 1 comparison was been made
        self.assertEqual(table.comparisons_used, 1)

    def test_add2_and_find2(self):
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        table.store_pair(fee, (123, True))
        table.store_pair(jo, (567, True))
        self.assertEqual(table.get_value(fee), (123, True))
        self.assertEqual(table.get_value(jo), (567, True))
        # think about why 3 comparisons were been made
        self.assertEqual(table.comparisons_used, 3)

    def test_add2_and_not_find1(self):
        # note: fee, jo, and bee all hash to the same slot
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        bee = Name('Bee')
        # note using simple values :)
        table.store_pair(fee, 1)
        table.store_pair(jo, 2)
        self.assertIsNone(table.get_value(bee))
        # think about why 2 comparisons have been made
        self.assertEqual(table.comparisons_used, 2)

    def test_add3_and_find1_v1(self):
        # note: fee, jo, and bee all hash to the same slot
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        bee = Name('Bee')
        # note using simple values :)
        table.store_pair(fee, 1)
        table.store_pair(jo, 2)
        table.store_pair(bee, 3)
        self.assertEqual(table.get_value(fee), 1)
        # think about why 3 comparisons have been made
        self.assertEqual(table.comparisons_used, 3)

    def test_add3_and_find1_v2(self):
        # note: fee, jo, and bee all hash to the same slot
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        bee = Name('Bee')
        # note using simple values :)
        table.store_pair(fee, 1)
        table.store_pair(jo, 2)
        table.store_pair(bee, 3)
        self.assertEqual(table.get_value(bee), 3)
        self.assertEqual(table.comparisons_used, 1)

    def test_add3_and_find1_v3(self):
        # note: fee and jo hash to the same slot, dee hashes to another
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        dee = Name('Dee')
        # note using simple values :)
        table.store_pair(fee, 1)
        table.store_pair(jo, 2)
        table.store_pair(dee, 3)
        self.assertEqual(table.get_value(fee), 1)
        self.assertEqual(table.comparisons_used, 2)

    def test_add3_and_find3_v1(self):
        # note: fee and jo hash to the same slot, dee hashes to another
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        dee = Name('Dee')
        # note using simple values :)
        table.store_pair(fee, 1)
        table.store_pair(jo, 2)
        table.store_pair(dee, 3)
        self.assertEqual(table.get_value(fee), 1)
        self.assertEqual(table.comparisons_used, 2)
        self.assertEqual(table.get_value(jo), 2)
        self.assertEqual(table.comparisons_used, 3)
        self.assertEqual(table.get_value(dee), 3)
        self.assertEqual(table.comparisons_used, 4)

    def test_update_key_value_pair(self):
        # note: fee, jo, and bee all hash to the same slot
        # adding a key twice will effectively
        # update the key value pair
        # note, you can assume that our testing of your
        # function for looking up results won't have
        # any duplicate keys...
        table = HashTable(11)
        fee = Name('Fee')
        jo = Name('Jo')
        bee = Name('Bee')
        # note using simple values :)
        table.store_pair(fee, 1)
        table.store_pair(jo, 2)
        table.store_pair(bee, 3)
        self.assertEqual(table.get_value(fee), 1)
        # update value for fee to 7
        table.store_pair(fee, 7)
        self.assertEqual(table.get_value(fee), 7)
        # think about why 4 comparisons are used
        self.assertEqual(table.comparisons_used, 4)



# ------------------------------------------------------------------------------
# These tests test your hash_result_finder function
class BaseTestsHash(BaseTests):

    def setUp(self):
        super().setUp()
        self.function_to_test = hash_result_finder
        self.load_factor = 0.5
        Name.reset_hashes()
        HashTable.reset_memory_used()

    def memory_test(self, test_filename, bound):
        HashTable.reset_memory_used()
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, quarantined_results = read_test_data(
            test_file_location)
        results, comparisons = self.function_to_test(tested,
                                                 quarantined)
        self.assertEqual(HashTable.get_memory_used(), bound)

    def hash_test(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, quarantined_results = read_test_data(
            test_file_location)
        results, comparisons = self.function_to_test(tested,
                                                 quarantined)
        expected = len(tested) + len(quarantined)
        self.assertEqual(Name.get_hashes(), expected)

    def get_bounds(self, tested_size, quarantined_size, intersection_size):
        if tested_size == 0 or quarantined_size == 0:
            lower_bound = upper_bound = 0
        else:
            load_factor = self.load_factor
            # the fudge_factor used to allow for sample variation
            # in smaller tests where the average is not very useful...
            if quarantined_size <= 10:
                fudge_factor = 4
            else:
                fudge_factor = 2
            lower_bound = intersection_size if intersection_size > 0 else 0
            num_failed_searches = (quarantined_size - intersection_size)
            num_successful_searches = intersection_size
            avg_comps_failed_searches = num_failed_searches * self.load_factor
            avg_one_successful_search = 1 + load_factor/2 - load_factor/(2*tested_size)
            avg_comps_successful_searches = num_successful_searches * avg_one_successful_search
            upper_bound = (avg_comps_failed_searches + avg_comps_successful_searches)
            upper_bound *= fudge_factor
        return lower_bound, upper_bound

    def result_list_test(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined, self.load_factor)
        self.AssertListsEqual(results, expected_results)
        self.assertEqual(type(results), type(expected_results))

    def comparisons_test(self, test_filename, expected_comparisons):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined, self.load_factor)
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but was expected to use {expected_comparisons}."
        self.assertEqual(comparisons, expected_comparisons, msg=message)

    def internal_comparisons_test(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined, self.load_factor)
        actual_comparisons = actual_count(NAME_COMPS)
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but it actually used {actual_comparisons}. "
        message += "This means you are miscounting Name comparisons, eg, "
        message += "not counting Name comparisons when they are made or "
        message += "counting Name comparisons that weren't made."
        self.assertEqual(comparisons, actual_count(NAME_COMPS))

    def comparisons_within_bound_test(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined, self.load_factor)
        intersect_size = intersect_size_from_filename(test_filename)
        lower_bound, upper_bound = self.get_bounds(len(tested),
                                                   len(quarantined),
                                                   intersect_size)
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but was expected to use at least {lower_bound}."
        self.assertGreaterEqual(comparisons, lower_bound, msg=message)
        message2 = f"Your code reported using {comparisons} Name comparisons "
        message2 += f"but was expected to use no more than {upper_bound}."
        self.assertLessEqual(comparisons, upper_bound, msg=message2)


    def hash_tables_created_check(self, test_filename):
        """ Should make just one hash table of specified size """
        tested_size = tested_size_from_filename(test_filename)
        expected = 1 if tested_size > 0 else 0
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, quarantined_results = read_test_data(
            test_file_location)
        results_found, comparisons = self.function_to_test(tested, quarantined)
        self.assertEqual(actual_count(HASH_TABLES_CREATED), expected)

    def AssertHashTablesEqual(table1, table2):
        """ Checks if the two hash tables are equal.
        The internal comparisons counter is turned off for this
        so it doesn't interfere with stuff you have done.
        """
        StatCounter.lock_counter(NAME_COMPS)
        self.assertEqual(table1, table2)
        StatCounter.unlock_counter(NAME_COMPS)




class TrivialHashTests(BaseTestsHash, TrivialListTest):
    pass


class SmallHashTests(BaseTestsHash, SmallTests):

    # the following is tested in addition to the
    # SmallTests tests
    def test_single_result_small_hash_count(self):
        filename = 'test_data-10i-10r-1-a.txt'
        self.hash_test(filename)


class SmallExactHashTests(BaseTestsHash):

    def setUp(self):
        super().setUp()

    def test_10_results_small(self):
        filename = 'test_data-10n-10n-10-a.txt'
        self.exact_comparisons_test(filename, 11)
        self.setUp()
        self.internal_comparisons_test(filename)

    def test_no_results_small_exact_comparisons(self):
        filename = 'test_data-10n-10n-0-a.txt'
        self.exact_comparisons_test(filename, 5)
        self.setUp()
        self.internal_comparisons_test(filename)

    def test_single_results_small_exact_comparisons(self):
        filename = 'test_data-10n-10n-1-a.txt'
        self.exact_comparisons_test(filename, 4)
        self.setUp()
        self.internal_comparisons_test(filename)

    def test_10_results_small_exact_comparisons(self):
        filename = 'test_data-10n-10n-10-a.txt'
        self.exact_comparisons_test(filename, 11)
        self.setUp()
        self.internal_comparisons_test(filename)


class MediumHashTests(BaseTestsHash, MediumTests):
    pass



class MediumHashLoadFactorTests(BaseTestsHash):

    def test_10_results_medium_quarter_load(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.load_factor = 0.25
        self.result_list_test(filename)

    def test_10_results_med_comps_in_bound_quarter_load(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.load_factor = 0.25
        self.comparisons_within_bound_test(filename)

    def test_10_results_med_internal_comps_quarter_load(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.load_factor = 0.25
        self.internal_comparisons_test(filename)



class BigHashTests(BaseTestsHash, BigTests):

    def test_all_found_large_memory(self):
        filename = 'test_data-1000i-1000r-10-a.txt'
        self.memory_test(filename, 3000)

    def test_single_result_large_hash_count(self):
        filename = 'test_data-1000i-1000r-1-a.txt'
        self.hash_test(filename)



class BigHashLoadFactorTests(BaseTestsHash):

    def test_10_results_big_quarter_load(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.load_factor = 0.25
        self.result_list_test(filename)

    def test_10_results_big_comps_in_bound_quarter_load(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.load_factor = 0.25
        self.comparisons_within_bound_test(filename)

    def test_10_results_big_internal_comps_quarter_load(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.load_factor = 0.25
        self.internal_comparisons_test(filename)

    def test_10_results_big_quarter_lambda_5(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.load_factor = 5
        self.result_list_test(filename)

    def test_10_results_big_comps_in_bound_lambda_5(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.load_factor = 5
        self.comparisons_within_bound_test(filename)

    def test_10_results_big_internal_comps_lambda_5(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.load_factor = 5
        self.internal_comparisons_test(filename)


class HugeHashTests(BaseTestsHash, HugeTests):
    pass


class GinormousHashTests(BaseTestsHash, GinormousTests):
    pass










class HelpfulDualTests(BaseTester):
    """
    NOTE: There are a few ways to order your comparisons when
    using this method. We require one order in particular.
    It will work well when the number of matches is small,
    which is what we would expect, ie, not many quarantined
    people have been tested.
    These test cases are designed to help you figure out which
    order of comparisons we require.
    Use pen and paper to help work out how we get the expected
    number of comparisons.
    """

    def setUp(self):
        """This runs before each test case"""
        super().setUp()
        self.function_to_test = dual_result_finder

    def test_dual_helpful_1(self):
        # See note in class docstring
        tested = [(1, Name('a'), True)]
        quarantined = make_name_list(['b'])
        expected_results = [(Name('b'), None, None)]
        student_results, comparisons = self.function_to_test(tested,
                                                 quarantined)
        self.AssertListsEqual(student_results, expected_results)
        expected_comparisons = 1
        self.assertEqual(comparisons, expected_comparisons)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))

    def test_dual_helpful_2(self):
        # See note in class docstring
        tested = [(1, Name('a'), True)]
        quarantined = make_name_list(['a'])
        expected_results = [(Name('a'), 1, True)]
        student_results, comparisons = self.function_to_test(tested,
                                                 quarantined)
        self.AssertListsEqual(student_results, expected_results)
        expected_comparisons = 2
        self.assertEqual(comparisons, expected_comparisons)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))

    def test_dual_helpful_3(self):
        # See note in class docstring
        tested = [(1, Name('a'), True),
                  (2, Name('b'), False)]
        quarantined = make_name_list(['b', 'c', 'e'])
        expected_results = [(Name('b'), 2, False),
                            (Name('c'), None, None),
                            (Name('e'), None, None)]
        student_results, comparisons = self.function_to_test(tested,
                                                 quarantined)
        self.AssertListsEqual(student_results, expected_results)
        expected_comparisons = 3
        self.assertEqual(comparisons, expected_comparisons)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))

    def test_dual_helpful_4(self):
        tested = [(1, Name('a'), True),
                  (2, Name('b'), False)]
        quarantined = make_name_list(['c', 'd', 'e'])
        expected_results = [(Name('c'), None, None),
                            (Name('d'), None, None),
                            (Name('e'), None, None)]
        student_results, comparisons = self.function_to_test(tested,
                                                 quarantined)
        self.AssertListsEqual(student_results, expected_results)
        expected_comparisons = 2
        self.assertEqual(comparisons, expected_comparisons)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))

    def test_dual_helpful_5(self):
        tested = [(1, Name('a'), True),
                  (2, Name('b'), False)]
        quarantined = make_name_list(['a', 'c', 'e'])
        expected_results = [(Name('a'), 1, True),
                            (Name('c'), None, None),
                            (Name('e'), None, None)]
        student_results, comparisons = self.function_to_test(tested,
                                                 quarantined)
        self.AssertListsEqual(student_results, expected_results)
        expected_comparisons = 3
        self.assertEqual(comparisons, expected_comparisons)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))



class BaseTestsDual(BaseTests):

    def setUp(self):
        super().setUp()
        self.function_to_test = dual_result_finder

    def get_bounds(self, tested_size, quarantined_size, intersect_size):
        lower_bound = min(tested_size, quarantined_size)
        upper_bound = max(0, 2 * (tested_size + quarantined_size - 1))
        return lower_bound, upper_bound


class TrivialDualTests(BaseTestsDual, TrivialListTest):
    pass


class SmallDualTests(BaseTestsDual, SmallTests):
    pass


class MediumDualTests(BaseTestsDual, MediumTests):
    pass


class BigDualTests(BaseTestsDual, BigTests):
    pass


class HugeDualTests(BaseTestsDual, HugeTests):
    pass


class GinormousDualTests(BaseTestsDual, GinormousTests):
    pass


class DualTestsExact(BaseTestsDual):

    def setUp(self):
        super().setUp()

    def test_10n_10n_0_exact_comps(self):
        filename = 'test_data-10n-10n-0-a.txt'
        self.result_list_test(filename)
        self.setUp()
        self.comparisons_test(filename, 25)
        self.setUp()
        self.internal_comparisons_test(filename)

    def test_10n_10n_1_exact_comps(self):
        filename = 'test_data-10n-10n-1-a.txt'
        self.result_list_test(filename)
        self.setUp()
        self.comparisons_test(filename, 23)
        self.setUp()
        self.internal_comparisons_test(filename)

    def test_10n_10n_10_exact_comps(self):
        filename = 'test_data-10n-10n-10-a.txt'
        self.result_list_test(filename)
        self.setUp()
        self.comparisons_test(filename, 20)
        self.setUp()
        self.internal_comparisons_test(filename)

    def test_50n_10n_1_exact_comps(self):
        filename = 'test_data-50n-10n-1-a.txt'
        self.result_list_test(filename)
        self.setUp()
        self.comparisons_test(filename, 60)
        self.setUp()
        self.internal_comparisons_test(filename)

    def test_50n_10n_5_exact_comps(self):
        filename = 'test_data-50n-10n-5-a.txt'
        self.result_list_test(filename)
        self.setUp()
        self.comparisons_test(filename, 63)
        self.setUp()
        self.internal_comparisons_test(filename)

    def test_50n_10n_10_exact_comps(self):
        filename = 'test_data-50n-10n-10-a.txt'
        self.result_list_test(filename)
        self.setUp()
        self.comparisons_test(filename, 58)
        self.setUp()
        self.internal_comparisons_test(filename)






def all_tests_suite():
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader.loadTestsFromTestCase
    # uncomment the following lines when you're
    # ready to run such tests

    # the following test your HashTable class
    suite.addTest(test_loader(TrivialHashTableTests))
    suite.addTest(test_loader(HashTableTests))

    # the following test your hash_result_finder function
    suite.addTest(test_loader(TrivialHashTests))
    suite.addTest(test_loader(SmallHashTests))
    suite.addTest(test_loader(MediumHashTests))
    suite.addTest(test_loader(MediumHashLoadFactorTests))
    suite.addTest(test_loader(BigHashTests))
    suite.addTest(test_loader(BigHashLoadFactorTests))
    suite.addTest(test_loader(HugeHashTests))
    suite.addTest(test_loader(SmallExactHashTests))
    suite.addTest(test_loader(GinormousHashTests))


    # the following test your dual_result_finder function
    # suite.addTest(test_loader(HelpfulDualTests))
    # suite.addTest(test_loader(TrivialDualTests))
    # suite.addTest(test_loader(SmallDualTests))
    # suite.addTest(test_loader(DualTestsExact))
    # suite.addTest(test_loader(MediumDualTests))
    # suite.addTest(test_loader(BigDualTests))
    # suite.addTest(test_loader(HugeDualTests))
    # suite.addTest(test_loader(GinormousDualTests))


    return suite




def main():
    """ Makes a test suite and runs it. Will your code pass? """
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)


if __name__ == '__main__':
    main()
