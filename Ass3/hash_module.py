"""
Module for looking up test results.
Students need to complete the get_value method for the HashTable
and then complete the hash_result_finder function
"""

from classes3 import Name, Node
from stats import StatCounter, HASH_TABLES_CREATED

# note you might want to import other things below for testing
# but your submission should only include the import lines above.


class HashTable:
    """A chaining hash table to store (key, value) pairs.
    You should use the default hash function for key objects as
    the basis for determining which slot items go/are in,
    eg, hash(key)
    In the assignment context the keys will be Names and values
    will be (nhi, result) tuples.
    You should be able to add other objects when testing,
    as long as they are hashable with hash(my_testing_thing)...
    But make sure you test it with Name objects as this will let
    you compare your comparisons_used with the actual comparisons used.
    ************************************************************************
    ************************************************************************
    *** DON'T add/remove/change any methods except the get_value method! ***
    ************************************************************************
    ************************************************************************
    """

    # class variables - used for keeping track of number of pointers used.
    # each slot uses one pointer to point ot the head of the linked list
    # in that slot and each node uses one pointer to point to the next node
    # This variable doesn't include memory used for the data in each node.
    _memory_used = 0

    def __init__(self, initial_size):
        """Initialises a hash table with initial_size slots.
        The slots are basically stored as a linked list of Nodes.
        The performance counters are all set to zero.
        """
        self.comparisons_used = 0
        self.number_of_slots = initial_size
        self._number_of_items = 0

        # setup the given number of slots, each containing None
        # Note: self._data[i] will be the head of a linked list
        self._data = [None] * initial_size
        HashTable._memory_used += initial_size
        StatCounter.increment(HASH_TABLES_CREATED)

    def store_pair(self, key, value):
        """
        Stores the key, value pair in the hash table.
        Uses the hash of the key to get the index to store the pair.
        You should make a new node using the given key and value and insert it
        at the start of the linked list in the indexed slot in self._data
        Notes:
        duplicate (key, value) pairs are dealt with by just inserting the
        new (key, value) pair at the start of the linked list instead of
        updating the (key, value) pair in the list. This saves time and
        effectively updates the value for the given key as the get_value
        method always returns the value associated with the first key found
        in the linked list.
        Don't worry too much about this as our tests will assume that there
        are no duplicate names in the tested list so duplicate (key, value)
        pairs won't occur in the main tests. It's just something to think about.
        """
        slot_index = hash(key) % self.number_of_slots
        head = self._data[slot_index]
        new_node = Node(key, value)
        if head is None:
            self._data[slot_index] = new_node
        else:
            new_node.next_node = head
            self._data[slot_index] = new_node
        self._number_of_items += 1
        HashTable._memory_used += 1

    def get_value(self, key):
        """Returns the first value associated with the key.
        If the key isn't in the table then None is returned.
        NOTE: Make sure you update self.comparisons_used so that
        it reflects the number of Name objects comparisons used.
        Hints:
        Which slot will name be in if it's in the table?
        How do you search the linked list in that slot?
        Example:
        if you stored a value of 10 for 'Bob' in my_table
        my_table.store('Bob', 10)
        then
        my_table.get_value('Bob') should return 10
        See the my_tests function below for some starter tests/examples.
        """
        # ---start student section---
        
        # ===end student section===

    def __repr__(self):
        """This is rather ugly, you are better to do a print(my_hashtable)
        which will use the __str__ method to give more readable output.
        """
        return repr(self._data)

    def __str__(self):
        string_thing = "HashTable:\n"
        for slot_index, head_node in enumerate(self._data):
            string_thing += f"{slot_index:6}: {repr(head_node)}\n"
        string_thing += f"Num of items = {self._number_of_items}\n"
        string_thing += f"Num of slots = {self.number_of_slots}\n"
        string_thing += f"Load factor  = {self.load_factor():.2f}"
        return string_thing

    def __contains__(self, item):
        """You aren't completing this method.
        You need to complete the contains method
        You could use the following instead (but you shouldn't need to):
            your_table.get_value(key_to_find) is not None
        """
        raise TypeError("You can't use the 'in' keyword with a HashTable")

    def load_factor(self):
        """Returns the load factor for the hash table"""
        return self._number_of_items / self.number_of_slots

    def index(self, start=None):
        """Points out that we can't do this!"""
        raise TypeError(f"{type(self)} doesn't allow using index")

    def __getitem__(self, i):
        """You can't directly index into HashTables, eg,
        ht = Hashtable(11)
        item0 = ht[0]  # won't work
        You should use your_table.get_value(key_to_find) instead.
        """
        raise IndexError("You can't directly index into Hashtables")

    @classmethod
    def get_memory_used(cls):
        """Returns the amount of memory used"""
        return cls._memory_used

    @classmethod
    def reset_memory_used(cls):
        """Resets the the memory tracker"""
        cls._memory_used = 0


# ----------------- End of HashTable class ----------------------------


def hash_result_finder(tested, quarantined, load_factor=0.5):
    """The tested list contains (nhi, Name, result) tuples
    and isn't guaranteed to be in any order
    quarantined is a list of Name objects
    and isn't guaranteed to be in any order
    This function should return a list of (Name, nhi, result)
    tuples and the number of comparisons made.
    The result list must be in the same order
    as the quarantined list.

    Obviously you will use a Hashtable to complete this task.
    The keys in the hash table will be Names and the values
    will be (nhi, result) pairs.

    The hashtable is initialised such that adding the people from the
    tested list will result in a load factor of approximately load_factor,
    with the default load_factor set to 0.5.
    That is, the table size is set to be len(tested) // load_factor
    **** NOTE: Remember to complete the HashTable definition above!
    """
    if len(tested) > 0:
        table_size = int(len(tested) / load_factor)
        hash_table = HashTable(table_size)
    # think about how to generate results list if tested is empty
    #    Hint: you don't want to generate a hash table with size 0...
    results = []
    # ---start student section---
    pass
    # ===end student section===
    # hint: you can get comparisons from the hash_table if one was used.
    return results, comparisons


def my_tests():
    """put your own simple tests here.
    You don't need to submit this code
    """
    table = HashTable(11)
    table.store_pair(Name("Lee"), (123, True))
    table.store_pair(Name("Bee"), (234, True))
    table.store_pair(Name("Gee"), (567, True))
    table.store_pair(Name("Fee"), (235, True))
    # Bee had another test and is now clear :)
    table.store_pair(Name("Bee"), (234, False))
    print(table)
    print("Bee's value =", table.get_value(Name("Bee")))  # should get (234, False)

    print("Add more tests here...")


if __name__ == "__main__":
    my_tests()
