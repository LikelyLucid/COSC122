"""Module containing the unit tests for the result getting functions."""
import os
import shutil
import tools
import unittest
import math
import random
import json
import sys
import time
from classes2 import Name, BstNode, bst_nested_repr
from bst_module import *
#from hash_module import HashTable, hash_result_finder
from stats import IS_MARKING_MODE, NAME_COMPS, StatCounter
from tools import read_test_data, make_name_list, make_tested_list

sys.setrecursionlimit(10**6)

actual_count = StatCounter.get_count
lock_counter = StatCounter.lock_counter
unlock_counter = StatCounter.unlock_counter
DATA_DIR = './test_data/'
SEED = 'a'


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


def read_expected_comps(filename):
    """ Reads a dictionary containing expected comparisons
    for each test data file with the given method from
    the given file.
    Returns a dictionary mapping data file names to comparisons.
    """
    full_filename = os.path.abspath(os.path.join(DATA_DIR, filename))
    with open(full_filename) as infile:
        data = infile.read()
        expected_comps_dict = json.loads(data)
    return expected_comps_dict


def read_tested_mins_and_maxs(filename):
    """ Reads a dictionary containing expected min and max names in
    the expected list in the given file
    Returns a dictionary mapping data file names to comparisons.
    """
    full_filename = os.path.abspath(DATA_DIR + filename)
    with open(full_filename) as infile:
        data = infile.read()
        expected_comps_dict = json.loads(data)
    return expected_comps_dict


# load as a global constants so file isn't loaded over and over :)
BST_EXPECTED_COMPS_FILENAME = 'expected_bst_comps.txt'
EXPECTED_MIN_MAX_FILENAME = 'expected_mins_and_maxs.txt'
SMART_BST_EXPECTED_COMPS_V1_FILENAME = 'expected_smart_bst_comps_v1.txt'
SMART_BST_EXPECTED_COMPS_V2_FILENAME = 'expected_smart_bst_comps_v2.txt'

if IS_MARKING_MODE:
    BST_EXPECTED_COMPS = "Can't use BST_EXPECTED_COMPS in marking mode!!!"
    SMART_BST_EXPECTED_COMPS_V1 = "Can't use SMART_BST_EXPECTED_COMPS_V1 in marking mode!!!"
    SMART_BST_EXPECTED_COMPS_V2 = "Can't use SMART_BST_EXPECTED_COMPS_V2 in marking mode!!!"
    EXPECTED_MINS_AND_MAXS = "Can't use EXPECTED_MINS_AND_MAXS in marking mode!!!"
else:
    BST_EXPECTED_COMPS = read_expected_comps(BST_EXPECTED_COMPS_FILENAME)
    SMART_BST_EXPECTED_COMPS_V1 = read_expected_comps(SMART_BST_EXPECTED_COMPS_V1_FILENAME)
    SMART_BST_EXPECTED_COMPS_V2 = read_expected_comps(SMART_BST_EXPECTED_COMPS_V2_FILENAME)
    EXPECTED_MINS_AND_MAXS = read_expected_comps(EXPECTED_MIN_MAX_FILENAME)


class BaseTester(unittest.TestCase):

    def setUp(self):
        """This runs before each test case"""
        unlock_counter(NAME_COMPS)
        StatCounter.reset_counts()
        self.start_time = time.perf_counter()
        # self.function_to_test should be setup by subclasses with the student function
        # that they want to test

    def tearDown(self):
        self.end_time = time.perf_counter()
        test_time = (self.end_time - self.start_time)
        print(f'{test_time:.4f}s', end=' ')

    def AssertListsEqual(self, list1, list2):
        """ Locks the counter when comparing lists """
        lock_counter(NAME_COMPS)
        self.assertEqual(list1, list2)
        unlock_counter(NAME_COMPS)

    def AssertListInOrder(self, alist):
        """ Checks to see if list is in order """
        lock_counter(NAME_COMPS)
        for i in range(1, len(alist)):
            self.assertLessEqual(alist[i - 1], alist[i])
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

    def exact_comparisons_test(self, test_filename):
        # checks vs an exact number of comparisons
        # as opposed to a range
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined)
        intersect_size = intersect_size_from_filename(test_filename)
        expected_comparisons = self.expected_comparisons_dict[test_filename]
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but was expected to use {expected_comparisons}."
        self.assertEqual(comparisons, expected_comparisons, msg=message)

    def internal_comparisons_test(self, test_filename):
        # checks that the reported/returned number of comparisons
        # equals the actual number of comparisons carried out
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

    def both_comparisons_test(self, test_filename):
        # checks vs an exact number of comparisons
        # and also checks that the reported comps matches actual comps
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        results, comparisons = self.function_to_test(tested, quarantined)
        intersect_size = intersect_size_from_filename(test_filename)
        expected_comparisons = self.expected_comparisons_dict[test_filename]
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but was expected to use {expected_comparisons}."
        self.assertEqual(comparisons, expected_comparisons, msg=message)
        actual_comparisons = actual_count(NAME_COMPS)
        message = f"Your code reported using {comparisons} Name comparisons "
        message += f"but it actually used {actual_comparisons}. "
        message += "This means you are miscounting Name comparisons, eg, "
        message += "not counting Name comparisons when they are made or "
        message += "counting Name comparisons that weren't made."
        self.assertEqual(comparisons, actual_comparisons, msg=message)


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

    def test_no_results_small_exact_comparisons(self):
        filename = 'test_data-10n-10n-0-a.txt'
        self.exact_comparisons_test(filename)

    def test_single_results_exact_comparisons(self):
        filename = 'test_data-10n-10n-1-a.txt'
        self.exact_comparisons_test(filename)

    def test_10_results_small_exact_comparisons(self):
        filename = 'test_data-10n-10n-10-a.txt'
        self.exact_comparisons_test(filename)

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
        filename = 'test_data-50n-50r-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_medium_exact_comparisons(self):
        filename = 'test_data-50n-50n-0-a.txt'
        self.exact_comparisons_test(filename)

    def test_no_results_medium_internal_comparisons(self):
        filename = 'test_data-50n-50n-0-a.txt'
        self.internal_comparisons_test(filename)

    def test_single_results_medium(self):
        filename = 'test_data-50n-50n-1-a.txt'
        self.result_list_test(filename)

    def test_single_results_medium_exact_comparisons(self):
        filename = 'test_data-50n-50n-1-a.txt'
        self.exact_comparisons_test(filename)

    def test_single_results_medium_internal_comparisons(self):
        filename = 'test_data-50n-50n-1-a.txt'
        self.internal_comparisons_test(filename)

    def test_10_results_medium(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_medium_exact_comparisons(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.exact_comparisons_test(filename)

    def test_10_results_medium_internal_comparisons(self):
        filename = 'test_data-50n-50n-10-a.txt'
        self.internal_comparisons_test(filename)


class BigTests(BaseTests):

    def setUp(self):
        super().setUp()

    def test_no_results_big(self):
        filename = 'test_data-1000i-1000n-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_big_exact_comparisons(self):
        filename = 'test_data-1000i-1000n-0-a.txt'
        self.exact_comparisons_test(filename)

    def test_single_results_big(self):
        filename = 'test_data-1000i-1000n-1-a.txt'
        self.result_list_test(filename)

    def test_single_results_big_exact_comparisons(self):
        filename = 'test_data-1000i-1000n-1-a.txt'
        self.exact_comparisons_test(filename)

    def test_single_results_big_internal_comparisons(self):
        filename = 'test_data-1000i-1000n-1-a.txt'
        self.internal_comparisons_test(filename)

    def test_10_results_big(self):
        filename = 'test_data-1000i-1000n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_big_exact_comparisons(self):
        filename = 'test_data-1000i-1000n-10-a.txt'
        self.exact_comparisons_test(filename)

    def test_10_results_big_internal_comparisons(self):
        filename = 'test_data-1000i-1000n-10-a.txt'
        self.internal_comparisons_test(filename)

        # and some bad ones
    def test_10_results_big_bad(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_big_bad_exact_comparisons(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.exact_comparisons_test(filename)

    def test_10_results_big_bad_internal_comparisons(self):
        filename = 'test_data-1000n-1000n-10-a.txt'
        self.internal_comparisons_test(filename)


class HugeTests(BaseTests):

    def setUp(self):
        super().setUp()

    def test_no_results_huge(self):
        filename = 'test_data-10000i-50n-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_huge_both_comparisons(self):
        filename = 'test_data-10000i-50n-0-a.txt'
        self.exact_comparisons_test(filename)

    def test_single_results_huge(self):
        filename = 'test_data-10000i-50n-1-a.txt'
        self.result_list_test(filename)

    def test_single_results_huge_both_comparisons(self):
        filename = 'test_data-10000i-50n-1-a.txt'
        self.both_comparisons_test(filename)

    def test_10_results_huge(self):
        filename = 'test_data-10000i-50n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_huge_both_comparisons(self):
        filename = 'test_data-10000i-50n-10-a.txt'
        self.both_comparisons_test(filename)

    def test_10_results_huge(self):
        filename = 'test_data-10000i-50n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_huge_both_comparisons(self):
        filename = 'test_data-10000i-50n-10-a.txt'
        self.both_comparisons_test(filename)


class HugeSortedTests(BaseTests):

    def test_10_results_huge_sorted(self):
        filename = 'test_data-10000n-50n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_huge_both_comparisons_sorted(self):
        filename = 'test_data-10000n-50n-10-a.txt'
        self.both_comparisons_test(filename)


class GinormousTests(BaseTests):

    def setUp(self):
        super().setUp()

    def test_no_results_ginormous_bad(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = 'test_data-10000n-1000n-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_ginormous_bad_both_comparisons(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = 'test_data-10000n-1000n-0-a.txt'
        self.both_comparisons_test(filename)

    def test_single_result_ginormous_bad(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = 'test_data-10000n-1000n-1-a.txt'
        self.result_list_test(filename)

    def test_single_result_ginormous_bad_both_comparisons(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = 'test_data-10000n-1000n-1-a.txt'
        self.both_comparisons_test(filename)

    def test_10_results_ginormous_bad(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = 'test_data-10000n-1000n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_ginormous_bad_both_comparisons(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = 'test_data-10000n-1000n-10-a.txt'
        self.both_comparisons_test(filename)

    def test_no_results_ginormous_good(self):
        # notice how much quicker this is, thanks to a more balanced tree :)
        filename = 'test_data-10000i-1000n-0-a.txt'
        self.result_list_test(filename)

    def test_no_results_ginormous_good_exact_comparisons(self):
        filename = 'test_data-10000i-1000n-0-a.txt'
        self.exact_comparisons_test(filename)

    def test_single_results_ginormous_good(self):
        filename = 'test_data-10000i-1000n-1-a.txt'
        self.result_list_test(filename)

    def test_single_results_ginormous_good_exact_comparisons(self):
        filename = 'test_data-10000i-1000n-1-a.txt'
        self.exact_comparisons_test(filename)

    def test_single_results_ginormous_good_internal_comparisons(self):
        filename = 'test_data-10000i-10000n-1-a.txt'
        self.internal_comparisons_test(filename)

    def test_10_results_ginormous_good_exact_comparisons(self):
        filename = 'test_data-10000i-1000n-10-a.txt'
        self.exact_comparisons_test(filename)

    def test_10_results_ginormous_good(self):
        filename = 'test_data-10000i-1000n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_ginormous_good_internal_comparisons(self):
        filename = 'test_data-10000i-1000n-10-a.txt'
        self.internal_comparisons_test(filename)


class AreYouKiddingMeTests(BaseTests):
    # You can expect these tests to take a long time...
    # You should see a massive difference when compared
    # to files such as test_data-100000i-10000r-1-a.txt etc

    def setUp(self):
        super().setUp()

    def test_single_result_are_you_kidding_me(self):
        filename = 'test_data-100000n-10000n-1-a.txt'
        self.result_list_test(filename)

    def test_single_result_are_you_kidding_me_both_comparisons(self):
        filename = 'test_data-100000n-10000n-1-a.txt'
        self.both_comparisons_test(filename)

    def test_10_results_are_you_kidding_me_(self):
        filename = 'test_data-100000n-10000n-10-a.txt'
        self.result_list_test(filename)

    def test_10_results_are_you_kidding_me_both_comparisons(self):
        filename = 'test_data-100000n-10000n-10-a.txt'
        self.both_comparisons_test(filename)

    def test_10000_results_are_you_kidding_me_(self):
        filename = 'test_data-100000n-10000n-10000-a.txt'
        self.result_list_test(filename)

    def test_10000_results_are_you_kidding_me_both_comparisons(self):
        filename = 'test_data-100000n-10000n-10000-a.txt'
        self.both_comparisons_test(filename)


class SimpleBstStoreTests(BaseTester):

    def test_store_in_uninode_tree_v1(self):
        bst = BstNode(Name('Lee'), (1234, False))
        name_to_add = Name('Aby')
        value_to_add = (1235, True)
        comparisons = bst_store_pair(bst, name_to_add, value_to_add)
        self.assertEqual(comparisons, 1)
        self.assertEqual(bst.left.key, name_to_add)
        self.assertEqual(bst.left.value, value_to_add)

    def test_store_in_uninode_tree_v2(self):
        bst = BstNode(Name('Lee'), (1234, False))
        name_to_add = Name('Zoe')
        value_to_add = (1235, True)
        comparisons = bst_store_pair(bst, name_to_add, value_to_add)
        self.assertEqual(comparisons, 2)
        self.assertEqual(bst.right.key, name_to_add)
        self.assertEqual(bst.right.value, value_to_add)

    def test_store_2_in_uninode_tree_v1(self):
        bst = BstNode(Name('Lee'), (1234, False))
        name1_to_add = Name('Dee')
        value1_to_add = (1235, True)
        comparisons = bst_store_pair(bst, name1_to_add, value1_to_add)
        self.assertEqual(comparisons, 1)
        self.assertEqual(bst.left.key, name1_to_add)
        self.assertEqual(bst.left.value, value1_to_add)

        name2_to_add = Name('Zee')
        value2_to_add = (1236, True)
        comparisons = bst_store_pair(bst, name2_to_add, value2_to_add)
        self.assertEqual(comparisons, 2)
        self.assertEqual(bst.right.key, name2_to_add)
        self.assertEqual(bst.right.value, value2_to_add)

    def test_store_2_in_uninode_tree_v1(self):
        bst = BstNode(Name('Lee'), (1234, False))
        name_to_add = Name('Dee')
        value_to_add = (1235, True)
        comparisons = bst_store_pair(bst, name_to_add, value_to_add)
        self.assertEqual(comparisons, 1)
        self.assertEqual(bst.left.key, name_to_add)
        self.assertEqual(bst.left.value, value_to_add)

        name_to_add = Name('Zee')
        value_to_add = (1236, True)
        comparisons = bst_store_pair(bst, name_to_add, value_to_add)
        self.assertEqual(comparisons, 2)
        self.assertEqual(bst.right.key, name_to_add)
        self.assertEqual(bst.right.value, value_to_add)

    def test_store_2_in_uninode_tree_v2(self):
        bst = BstNode(Name('Lee'), (1234, False))
        name1 = Name('Dee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        self.assertEqual(comparisons, 1)
        self.assertEqual(bst.left.key, name1)
        self.assertEqual(bst.left.value, value1)

        name2 = Name('Bee')
        value2 = (1236, True)
        comparisons = bst_store_pair(bst, name2, value2)
        self.assertEqual(comparisons, 2)
        self.assertEqual(bst.left.key, name1)
        self.assertEqual(bst.left.value, value1)
        self.assertEqual(bst.left.left.key, name2)
        self.assertEqual(bst.left.left.value, value2)

    def test_store_2_in_uninode_tree_v3(self):
        bst = BstNode(Name('Lee'), (1234, False))
        name1 = Name('Dee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        self.assertEqual(comparisons, 1)
        self.assertEqual(bst.left.key, name1)
        self.assertEqual(bst.left.value, value1)

        name2 = Name('Gee')
        value2 = (1236, True)
        comparisons = bst_store_pair(bst, name2, value2)
        self.assertEqual(comparisons, 3)
        self.assertEqual(bst.left.key, name1)
        self.assertEqual(bst.left.value, value1)
        self.assertEqual(bst.left.right.key, name2)
        self.assertEqual(bst.left.right.value, value2)

    def test_store_2_in_uninode_tree_v4(self):
        bst = BstNode(Name('Lee'), (1234, False))
        name1 = Name('Mee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        self.assertEqual(comparisons, 2)
        self.assertEqual(bst.right.key, name1)
        self.assertEqual(bst.right.value, value1)

        name2 = Name('Zee')
        value2 = (1236, True)
        comparisons = bst_store_pair(bst, name2, value2)
        self.assertEqual(comparisons, 4)
        self.assertEqual(bst.right.key, name1)
        self.assertEqual(bst.right.value, value1)
        self.assertEqual(bst.right.right.key, name2)
        self.assertEqual(bst.right.right.value, value2)

    def test_update_value_in_two_node_tree(self):
        # storing a new value for name1 should mean that
        # the node is updated with the new value
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        name1 = Name('Zee')
        value1 = (1235, True)
        value2 = (4321, False)
        comparisons = bst_store_pair(bst, name1, value1)
        comparisons += bst_store_pair(bst, name1, value2)
        self.assertEqual(bst.right.key, name1)
        self.assertEqual(bst.right.value, value2)

    def test_update_value_in_two_node_tree_comps(self):
        # storing a new value for name1 should mean that
        # the node is updated with the new value
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        name1 = Name('Zee')
        value1 = (1235, True)
        value2 = (4321, False)
        comparisons = bst_store_pair(bst, name1, value1)
        comparisons += bst_store_pair(bst, name1, value2)
        self.assertEqual(comparisons, 6)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))
        self.assertEqual(bst.right.key, name1)
        self.assertEqual(bst.right.value, value2)


class SimpleGetValueTests(BaseTester):
    # Note: This testing assumes bst_store_pair is working
    #       Errors in bst_store_pair will causes errors here

    def test_get_value_in_uninode_tree_v1(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        value, comparisons = get_value_from_tree(bst, name0)
        self.assertEqual(comparisons, 2)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))
        self.assertEqual(value, value0)

    def test_get_value_in_two_node_tree_v1(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        name1 = Name('Bee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        StatCounter.reset_counts()
        value, comparisons = get_value_from_tree(bst, name1)
        self.assertEqual(comparisons, 3)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))
        self.assertEqual(value, value1)

    def test_get_value_in_two_node_tree_v2(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        name1 = Name('Zee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        StatCounter.reset_counts()
        value, comparisons = get_value_from_tree(bst, name1)
        self.assertEqual(comparisons, 4)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))
        self.assertEqual(value, value1)

    def test_get_value_in_3_node_trees(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        name1 = Name('Bee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        name2 = Name('Dee')
        value2 = (1236, False)
        comparisons = bst_store_pair(bst, name2, value2)

        StatCounter.reset_counts()
        value, comparisons = get_value_from_tree(bst, name2)
        self.assertEqual(comparisons, 5)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))
        self.assertEqual(value, value2)

        # try another variation of 3 node tree
        bst = BstNode(name0, value0)
        name1 = Name('Dee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        name2 = Name('Bee')
        value2 = (1236, False)
        comparisons = bst_store_pair(bst, name2, value2)

        StatCounter.reset_counts()
        value, comparisons = get_value_from_tree(bst, name2)
        self.assertEqual(comparisons, 4)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))
        self.assertEqual(value, value2)

        # and another variation of 3 node tree
        bst = BstNode(name0, value0)
        name1 = Name('Mee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        name2 = Name('Zee')
        value2 = (1236, False)
        comparisons = bst_store_pair(bst, name2, value2)

        StatCounter.reset_counts()
        value, comparisons = get_value_from_tree(bst, name2)
        self.assertEqual(comparisons, 6)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))
        self.assertEqual(value, value2)

        # and another variation of 3 node tree
        bst = BstNode(name0, value0)
        name1 = Name('Zee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        name2 = Name('Mee')
        value2 = (1236, False)
        comparisons = bst_store_pair(bst, name2, value2)

        StatCounter.reset_counts()
        value, comparisons = get_value_from_tree(bst, name2)
        self.assertEqual(comparisons, 5)
        self.assertEqual(comparisons, actual_count(NAME_COMPS))
        self.assertEqual(value, value2)


class SimpleBstNodeCountTests(BaseTester):

    def test_num_nodes_1(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        count = num_nodes_in_tree(bst)
        self.assertEqual(count, 1)

    def test_num_nodes_2(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        name1 = Name('Bee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        size = num_nodes_in_tree(bst)
        self.assertEqual(size, 2)

        # and another 2 node tree
        bst = BstNode(name0, value0)
        name1 = Name('Zee')
        value1 = (1235, True)
        comparisons = bst_store_pair(bst, name1, value1)
        size = num_nodes_in_tree(bst)
        self.assertEqual(size, 2)

    def test_num_nodes_10(self):
        # try with all nodes to right
        bst = BstNode(0, 0)
        for i in range(1, 10):
            bst_store_pair(bst, i, i)
            size = num_nodes_in_tree(bst)
            self.assertEqual(size, i + 1)
        # try with all nodes to left
        bst = BstNode(10, 10)
        for i in range(9, 0, -1):
            bst_store_pair(bst, i, i)
            size = num_nodes_in_tree(bst)
            self.assertEqual(size, 11 - i)

    def num_nodes_100(self):
        # try with all nodes to right
        bst = BstNode(0, 0)
        for i in range(1, 100):
            bst_store_pair(bst, i, i)
        size = num_nodes_in_tree(bst)
        self.assertEqual(size, 100)
        # try with all nodes to left
        bst = BstNode(100, 100)
        for i in range(99, 0, -1):
            bst_store_pair(bst, i, i)
        size = num_nodes_in_tree(bst)

        self.assertEqual(size, 100)

    def test_num_nodes_100_random(self):
        nums = list(range(100))
        random.shuffle(nums)
        bst = BstNode(nums[0], 0)
        for i in range(1, 100):
            bst_store_pair(bst, nums[i], i)
            size = num_nodes_in_tree(bst)
            self.assertEqual(size, i + 1)

    def test_num_nodes_1000_random(self):
        nums = list(range(1000))
        random.shuffle(nums)
        bst = BstNode(nums[0], 0)
        for i in range(1, 1000):
            bst_store_pair(bst, nums[i], i)
        size = num_nodes_in_tree(bst)
        self.assertEqual(size, 1000)


class SimpleBstDepthTests(BaseTester):

    def test_depth_1(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        depth = bst_depth(bst)
        self.assertEqual(depth, 0)

    def test_depth_10(self):
        # try with all nodes to right
        bst = BstNode(0, 0)
        for i in range(1, 11):
            bst_store_pair(bst, i, i)
            depth = bst_depth(bst)
            self.assertEqual(depth, i)
        # try with all nodes to left
        bst = BstNode(11, 0)
        for i in range(10, 0, -1):
            bst_store_pair(bst, i, i)
            depth = bst_depth(bst)
            self.assertEqual(depth, 11 - i)
        # try with 10 nodes to left and right
        for i in range(1, 11):
            bst_store_pair(bst, i, i)
        depth = bst_depth(bst)
        self.assertEqual(depth, 10)

    def test_depth_zig_zag(self):
        # start with 5 to the right
        bst = BstNode(0, 0)
        for i in range(100, 600, 100):
            bst_store_pair(bst, i, i)
        depth = bst_depth(bst)
        self.assertEqual(depth, 5)
        # add 5 nodes to left of last node
        for i in range(490, 440, -10):
            bst_store_pair(bst, i, i)
        depth = bst_depth(bst)
        self.assertEqual(depth, 10)
        # add 5 nodes to right of last node
        for i in range(440, 445, 1):
            bst_store_pair(bst, i, i)
        depth = bst_depth(bst)
        self.assertEqual(depth, 15)

    def test_depth_medium(self):
        # start with 5 to the right
        bst = BstNode(90, 0)
        for i in range(100, 600, 100):
            bst_store_pair(bst, i, i)
        depth = bst_depth(bst)
        self.assertEqual(depth, 5)
        # add 5 nodes to left
        for i in range(80, 30, -10):
            bst_store_pair(bst, i, i)
        depth = bst_depth(bst)
        self.assertEqual(depth, 5)
        # add 3 nodes to right of last node
        for i in range(600, 900, 100):
            bst_store_pair(bst, i, i)
        depth = bst_depth(bst)
        self.assertEqual(depth, 8)
        bst = BstNode(50, 0)
        for i in [40, 30, 60, 45, 44, 59, 80, 58, 70, 90, 71]:
            bst_store_pair(bst, i, i)
        depth = bst_depth(bst)
        self.assertEqual(depth, 4)



class SimpleBstMinTests(BaseTester):

    def test_bst_min_1(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, name0)

    def test_bst_min_2a(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        name1 = Name('Bee')
        value1 = (5431, False)
        bst = BstNode(name0, value0)
        bst_store_pair(bst, name1, value1)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, name1)

    def test_bst_min_2b(self):
        name0 = Name('Bee')
        value0 = (1234, False)
        name1 = Name('Lee')
        value1 = (5431, False)
        bst = BstNode(name0, value0)
        bst_store_pair(bst, name1, value1)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, name0)

    def test_bst_min_10(self):
        # try with all nodes to right
        bst = BstNode(0, 0)
        for i in range(1, 11):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 0)
        # try with all nodes to left
        bst = BstNode(11, 0)
        for i in range(10, 0, -1):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 1)
        # try with 10 nodes to left and right
        for i in range(12, 22):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 1)

    def test_bst_min_zig_zag(self):
        # start with 5 to the right
        bst = BstNode(0, 0)
        for i in range(100, 600, 100):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 0)
        # add 5 nodes to left of last node
        for i in range(490, 440, -10):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 0)
        # add 5 nodes to right of last node
        for i in range(440, 445, 1):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 0)

        # zig zag the other way
        # start with 5 to the left
        bst = BstNode(600, 0)
        for i in range(500, 0, -100):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 100)
        # add 5 nodes to right of last node
        for i in range(110, 160, 10):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 100)
        # add 5 nodes to left of last node
        for i in range(159, 154, -1):
            bst_store_pair(bst, i, i)
        min_key = min_key_in_bst(bst)
        self.assertEqual(min_key, 100)

    def test_bst_min_mish_mash(self):
        data = [52, 75, 43, 89, 22, 75, 65, 11, 99]
        bst = BstNode(data[0], 0)
        for i in range(1, len(data)):
            bst_store_pair(bst, data[i], i)
            min_key = min_key_in_bst(bst)
            self.assertEqual(min_key, min(data[:i + 1]))
        self.assertEqual(bst.left.left.key, 22)
        self.assertEqual(bst.right.right.key, 89)
        # another mish mash
        data = [200, 175, 243, 489, 122, 175, 165, 511, 267]
        bst = BstNode(200, 0)
        bst = BstNode(data[0], 0)
        for i in range(1, len(data)):
            bst_store_pair(bst, data[i], i)
            min_key = min_key_in_bst(bst)
            self.assertEqual(min_key, min(data[:i + 1]))
        self.assertEqual(bst.left.left.key, 122)
        self.assertEqual(bst.right.right.key, 489)


class SimpleBstMaxTests(BaseTester):

    def test_bst_max_1(self):
        name0 = Name('Lee')
        value0 = (1234, False)
        bst = BstNode(name0, value0)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, name0)

    def test_bst_max_10(self):
        # try with all nodes to right
        bst = BstNode(0, 0)
        for i in range(1, 11):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 10)
        # try with all nodes to left
        bst = BstNode(11, 0)
        for i in range(10, 0, -1):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 11)
        # try with 10 nodes to left and right
        for i in range(12, 22):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 21)

    def test_bst_max_zig_zag(self):
        # start with 5 to the right
        bst = BstNode(0, 0)
        for i in range(100, 600, 100):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 500)
        # add 5 nodes to left of last node
        for i in range(490, 440, -10):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 500)
        # add 5 nodes to right of last node
        for i in range(440, 445, 1):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 500)

        # zig zag the other way
        # start with 5 to the left
        bst = BstNode(6000, 0)
        for i in range(5000, 0, 1000):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 6000)
        # add 5 nodes to right of last node
        for i in range(1100, 1600, 10):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 6000)
        # add 5 nodes to left of last node
        for i in range(1590, 1540, -10):
            bst_store_pair(bst, i, i)
        max_key = max_key_in_bst(bst)
        self.assertEqual(max_key, 6000)

    def test_bst_max_mish_mash(self):
        data = [52, 75, 43, 89, 22, 75, 65, 11, 99]
        bst = BstNode(data[0], 0)
        for i in range(1, len(data)):
            bst_store_pair(bst, data[i], i)
            max_key = max_key_in_bst(bst)
            self.assertEqual(max_key, max(data[:i + 1]))
        self.assertEqual(bst.left.left.key, 22)
        self.assertEqual(bst.right.right.key, 89)
        # another mish mash
        data = [200, 175, 243, 489, 122, 175, 165, 511, 267]
        bst = BstNode(200, 0)
        bst = BstNode(data[0], 0)
        for i in range(1, len(data)):
            bst_store_pair(bst, data[i], i)
            max_key = max_key_in_bst(bst)
            self.assertEqual(max_key, max(data[:i + 1]))
        self.assertEqual(bst.left.left.key, 122)
        self.assertEqual(bst.right.right.key, 489)



class SimpleBstMinMaxTestsFromFiles(BaseTester):

    def bst_min_max_test(self, test_filename):
        expected_mins_and_maxes = EXPECTED_MINS_AND_MAXS
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        if tested:
            nhi, name, result = tested[0]
            bst = BstNode(name, (nhi, result))
            for i in range(1, len(tested)):
                nhi, name, result = tested[i]
                # print(name)
                bst_store_pair(bst, name, (nhi, result))
            min_name = min_key_in_bst(bst)._name
            max_name = max_key_in_bst(bst)._name
            #print(min_name, max_name)
            expected_min, expected_max = expected_mins_and_maxes[test_filename]
            self.assertEqual(min_name, expected_min)
            self.assertEqual(max_name, expected_max)

    def test_min_max_small_files(self):
        for filename in ['test_data-50i-50r-10-a.txt', 'test_data-10i-2r-2-a.txt',
                         'test_data-50i-50r-2-a.txt', 'test_data-50n-50r-5-a.txt',
                         'test_data-1000i-50n-1-a.txt', 'test_data-10000i-5r-1-a.txt']:
            self.bst_min_max_test(filename)


class SimpleBstInOrderTestFiles(BaseTester):

    def bst_in_order_test_small(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        tested, quarantined, expected_results = read_test_data(test_file_location)
        if tested:
            nhi, name, result = tested[0]
            bst = BstNode(name, (nhi, result))
            for i in range(1, len(tested)):
                nhi, name, result = tested[i]
                # print(name)
                bst_store_pair(bst, name, (nhi, result))
            # expect a list with the records in order
            sorted_tested = sorted(tested, key=lambda x: x[1])
            expected_list = [(name, (nhi, result)) for nhi, name, result in sorted_tested]
            StatCounter.reset_counts()
            student_answer_list = bst_in_order(bst)
            self.assertEqual(actual_count(NAME_COMPS), 0)
            self.AssertListInOrder(student_answer_list)
            self.AssertListsEqual(student_answer_list, expected_list)

    def test_in_order_small_files(self):
        for filename in ['test_data-50i-50r-10-a.txt', 'test_data-10i-2r-2-a.txt',
                         'test_data-50i-50r-2-a.txt', 'test_data-50n-50r-5-a.txt',
                         'test_data-1000i-50n-1-a.txt', 'test_data-10000i-5r-1-a.txt']:
            self.bst_in_order_test_small(filename)


# --------------------- Setup Tests for BSTs -----------------------------------
#-------------------------------------------------------------------------------


class BaseTestsBst(BaseTests):

    def setUp(self):
        super().setUp()
        self.function_to_test = bst_result_finder
        self.expected_comparisons_dict = BST_EXPECTED_COMPS



class TrivialBstTests(BaseTestsBst, TrivialListTest):
    pass


class SmallBstTests(BaseTestsBst, SmallTests):
    pass


class MediumBstTests(BaseTestsBst, MediumTests):
    pass


class BigBstTests(BaseTestsBst, BigTests):
    pass


class HugeBstTests(BaseTestsBst, HugeTests):
    pass


class HugeSortedBstTests(BaseTestsBst, HugeSortedTests):
    pass


class GinormousBstTests(BaseTestsBst, GinormousTests):
    pass


class AreYouKiddingMeBstTests(BaseTestsBst, AreYouKiddingMeTests):
    pass


class BaseTestsSmartBstV1(BaseTests):

    def setUp(self):
        super().setUp()
        self.function_to_test = smart_bst_result_finder_v1
        self.expected_comparisons_dict = SMART_BST_EXPECTED_COMPS_V1


class GinormousBstTestsV1(BaseTestsSmartBstV1, GinormousTests):
    pass


class AreYouKiddingMeSmartBstTestsV1(BaseTestsSmartBstV1, AreYouKiddingMeTests):
    pass


class BaseTestsSmartBstV2(BaseTests):

    def setUp(self):
        super().setUp()
        self.function_to_test = smart_bst_result_finder_v2
        self.expected_comparisons_dict = SMART_BST_EXPECTED_COMPS_V2


class GinormousBstTestsV2(BaseTestsSmartBstV2, GinormousTests):
    pass


class AreYouKiddingMeSmartBstTestsV2(BaseTestsSmartBstV2, AreYouKiddingMeTests):
    pass






def all_tests_suite():
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader.loadTestsFromTestCase
    # uncomment the following lines when you're
    # ready to run such tests

    # tests for bst functions
    suite.addTest(test_loader(SimpleBstStoreTests))
    suite.addTest(test_loader(SimpleGetValueTests))
    suite.addTest(test_loader(SimpleBstNodeCountTests))
    suite.addTest(test_loader(SimpleBstDepthTests))
    suite.addTest(test_loader(SimpleBstMinTests))
    suite.addTest(test_loader(SimpleBstMaxTests))
    suite.addTest(test_loader(SimpleBstMinMaxTestsFromFiles))
    suite.addTest(test_loader(SimpleBstInOrderTestFiles))

    # tests for result finder
    suite.addTest(test_loader(TrivialBstTests))
    suite.addTest(test_loader(SmallBstTests))
    suite.addTest(test_loader(MediumBstTests))
    suite.addTest(test_loader(HugeBstTests))
    suite.addTest(test_loader(HugeSortedBstTests))
    suite.addTest(test_loader(GinormousBstTests))
    # suite.addTest(test_loader(AreYouKiddingMeBstTests))

    # fun optional extras
    # these test optional extra fun bonus questions
    # and are not worth any marks
    # suite.addTest(test_loader(GinormousBstTestsV1))
    # suite.addTest(test_loader(AreYouKiddingMeSmartBstTestsV1))
    # suite.addTest(test_loader(GinormousBstTestsV2))
    # suite.addTest(test_loader(AreYouKiddingMeSmartBstTestsV2))

    return suite




def main():
    """ Makes a test suite and runs it. Will your code pass? """
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)


if __name__ == '__main__':
    main()



