"""
Have fun comparing various spellchecking methods
You should carefully follow the handout for this lab
so that you do things in the right order.
"""
import re
import os
from time import perf_counter
import doctest

# setup a ruled line string
LINE_WIDTH = 50
SINGLE_LINE = '-' * LINE_WIDTH


def print_line():
    """ Prints a single line """
    print(SINGLE_LINE)


def _c_mul(value_a, value_b):
    '''Substitute for c multiply function'''
    return ((int(value_a) * int(value_b)) & 0xFFFFFFFF)


def nice_hash(input_string):
    '''Takes a string name and returns a hash for the string. This hash value
    will be os independent, unlike the default Python hash function.'''
    if input_string is None:
        return 0  # empty
    value = ord(input_string[0]) << 7
    for char in input_string:
        value = _c_mul(1000003, value) ^ ord(char)
    value = value ^ len(input_string)
    if value == -1:
        value = -2
    return value


def longer_test_for_chaining():
    """
    NOTE: This will timeout on the quiz server if you are not
    using hashing properly
    Hint: You shouldn't be using a for loop
    in your __contains__ method!
    This test should take less than a second on your computer
    """
    table = ChainingHashTable(10000)
    table.store('banana')
    for i in range(100000):
        if 'zzzzzz' in table:
            print('How did zzzzzz get there?')
    print('Well done!')


# ---------------------------------------------
# Start of Class definitions
# ---------------------------------------------
class ChainingHashTable():
    """A simple HashTable.
    ***** IMPORTANT
    ***** =========
    ***** NOTE: These will fail initially, ie, when _hash returns 0
    ***** DON'T worry you will fix this later:
    >>> hash_table = ChainingHashTable(5)
    >>> hash_table.store('George')
    >>> hash_table.store('Bungle')
    >>> hash_table.store('Zippy')
    >>> hash_table.store('Jane')
    >>> hash_table.store('Rod')
    >>> hash_table.store('Freddy')
    >>> print(hash_table)
    ChainingHashTable:
    slot        0 = ['Rod']
    slot        1 = ['George', 'Jane']
    slot        2 = ['Bungle']
    slot        3 = ['Zippy', 'Freddy']
    slot        4 = []
    n_slots = 5
    n_items in table = 6
    Load factor =  1.200
    Average chain length = 1.200
    <BLANKLINE>
    NOTE: ChainingHashTable print doctests will fail initially, ie, when _hash returns 0
    Don't worry you will fix this later... See the The ChainingHashTable Class info panel
    <BLANKLINE>
    >>> print('Freddy' in hash_table)
    True
    >>> print('Dipsy' in hash_table)
    False
    >>> print('Joey' in hash_table)
    False
    >>> print('Jane' in hash_table)
    True
    >>> print('Bungle' in hash_table)
    True
    >>> longer_test_for_chaining()
    Well done!
    """

    def __init__(self, slots=11):
        """
        Creates a new hashtable with a number of slots (default: 11).
        It will help if you always make your hash table size a prime number.

        Each slot will contain a list of items that hash to the slot.
        Initially the list in each slot contains a None.
        n_items contains the number of items that have been put in the table.
        """
        self._data = [[] for i in range(slots)]
        self.n_slots = slots
        self.n_items = 0

    def _hash(self, item):
        """Computes the hash of an item.
        First calculate using nice_hash(item) and then use modulo
        to reduce it down to a number in the range 0..self.n_slots """
        old = False
        if old:
            return 0
        return nice_hash(item) % self.n_slots

    def store(self, item):
        """Appends an item to the list in the slot at _data[hash]."""
        index = self._hash(item)
        self._data[index].append(item)
        # Keep track of number of items in hash table
        self.n_items += 1

    def average_chain_length(self):
        """ Returns the average chain length """
        return self.n_items / self.n_slots

    def __str__(self):
        output = 'ChainingHashTable:\n'
        for i in range(self.n_slots):
            list_at_slot = self._data[i]
            output = output + f'slot {i:8d} = '
            if list_at_slot is None:
                output = output + 'None'
            else:
                output = output + str(list_at_slot)
            output += '\n'
        load_factor = float(self.n_items) / self.n_slots
        output += f'n_slots = {self.n_slots:d}\n'
        output += f'n_items in table = {self.n_items:d}\n'
        output += f'Load factor = {load_factor:6.3f}\n'
        output += f'Average chain length = {self.average_chain_length():.3f}\n'
        output += '\n'
        output += 'NOTE: ChainingHashTable print doctests will fail initially, ie, when _hash returns 0\n'
        output += "Don't worry you will fix this later... See the The ChainingHashTable Class info panel\n"
        return output


    def __contains__(self, item):
        """
        Checks to see if an item is stored within the hashtable.
        Returns True if it does, otherwise it returns False.
        You will need to call the self._hash(item) to find
        which slot the item would be in, if it's in the table.
        Then you will need to loop through the items in the
        chain list in that slot to see if the item is there.
        You can call this method using Python's 'in' keyword:
            ht = HashTable()
            ...
            if 'foo' in ht:
            ...
        """
        # Calculate the hash index for the item
        hashed_item_index = self._hash(item)

        # Retrieve the list at that slot
        slot_list = self._data[hashed_item_index]

        # Check if the item is in the list
        return item in slot_list


# ----------------------------------------------------------------------------
class LinearHashTable():
    """A simple Open Addressing HashTable with Linear Probing.
    Called simply LinearHashTable to make the name shorter...

    >>> hash_table = LinearHashTable(11)
    >>> print(hash_table._hash('Dingus'))
    2
    >>> print(hash_table._hash('Dirk'))
    6
    >>> hash_table.store('Dianna')
    >>> hash_table.store('Bobby')
    >>> hash_table.store('Dirk')
    >>> hash_table.store('Darlene')
    >>> hash_table.store('Paul')
    >>> hash_table.store('Peter')
    >>> hash_table.store('Paula')
    >>> hash_table.store('David')
    >>> hash_table.store('Mariana')
    >>> print(hash_table)
    LinearHashTable:
    slot        0 = David
    slot        1 = Darlene
    slot        2 = Paul
    slot        3 = Mariana
    slot        4 = Peter
    slot        5 = Paula
    slot        6 = Dirk
    slot        7 = -
    slot        8 = -
    slot        9 = Dianna
    slot       10 = Bobby
    n_slots = 11
    n_items in table = 9
    Load factor =  0.818
    <BLANKLINE>
    >>> 'Paul' in hash_table
    True
    >>> 'Peter' in hash_table
    True
    >>> 'Paula' in hash_table
    True
    >>> 'David' in hash_table
    True
    >>> 'Bobby' in hash_table
    True
    >>> 'Dianna' in hash_table
    True
    >>> 'Dirk' in hash_table
    True
    >>> 'Darlene' in hash_table
    True
    >>> 'Mariana' in hash_table
    True
    >>> print('Dingus' in hash_table)
    False
    """

    def __init__(self, slots=11):
        """
        Creates a new hashtable with the given number of slots.
        Remember we can't have a load factor greater than 1 for an open hash...
        """
        self._data = [None for i in range(slots)]
        self.n_slots = slots
        self.n_items = 0

    def _hash(self, item):
        """Return the hash of an item.
        First calculate using nice_hash(item) and then use modulo
        to reduce it down to a number in the range 0..self.n_slots
        """
        return nice_hash(item) % self.n_slots


    def store(self, item):
        """Stores an item in the hashtable."""
        if self.n_slots == self.n_items:
            # Argh - crash, who made the hashtable too small?
            print(self._data)
            print("Size = " + str(self.n_slots))
            print("Slots used = " + str(self.n_items))
            print("Whoops, hash table is full!!!!")
            print("In reality you would have made it bigger by now...")
            print("But, you're not expected to for this lab.")
            raise IndexError("Hash table is full!!!!")

        slot = self._hash(item)

        for i in range(self.n_slots):
            current_index = (slot + i) % self.n_slots
            if self._data[current_index] is None:
                self._data[current_index] = item
                self.n_items += 1
                break

    def __contains__(self, item):
        """
        Checks to see if an item is stored within the hashtable.
        Returns True if it does, otherwise it returns False.
        You can call this method using Python's 'in' keyword:
            ht = HashTable()
            ...
            print('foo' in ht)   # invoked ht.__contains__
                ...
        """
        first_hash = self._hash(item)
        found = False
        # check item at initial slot
        if self._data[first_hash] == item:
            found = True
        else:
            i = 1
            current_index = (first_hash + i) % self.n_slots
            while self._data[current_index] is not None and not found:
                if current_index == first_hash:
                    # back to original hash and didn't find item
                    # so give up
                    # phew - the hashtable is full!
                    break
                elif self._data[current_index] == item:
                    # horay we found it
                    found = True
                else:
                    # try next slot
                    i += 1
                    current_index = (first_hash + i) % self.n_slots
        return found

    def __str__(self):
        """ Returns a string representation of the hashtable
        Along with some summary stats.
        """
        output = 'LinearHashTable:\n'
        for i in range(self.n_slots):
            output += f'slot {i:8} = '
            item = self._data[i]
            if item is None:
                output = output + '-'
            else:
                output = output + str(item)
            output += '\n'
        load_factor = float(self.n_items) / self.n_slots
        output += f'n_slots = {self.n_slots}\n'
        output += f'n_items in table = {self.n_items}\n'
        output += f'Load factor = {load_factor:6.3f}\n'
        return output

    def __repr__(self):
        """ Just uses __str__ """
        return str(self)


# ----------------------------------------------------------------------------
class QuadraticHashTable():
    """Is a child class of OpenAddressHashTable.
    If a collision then uses a quadratic probing function to find a free slot
    >>> hash_table = QuadraticHashTable(11)
    >>> print(hash_table._hash('Dingus'))
    2
    >>> print(hash_table._hash('Dirk'))
    6
    >>> hash_table.store('Dianna')
    >>> hash_table.store('Bobby')
    >>> hash_table.store('Dirk')
    >>> hash_table.store('Darlene')
    >>> hash_table.store('Paul')
    >>> hash_table.store('Paula')
    >>> hash_table.store('David')
    >>> hash_table.store('Harry')
    >>> print(hash_table)
    QuadraticOpenAddressHashTable:
    slot        0 = David
    slot        1 = Darlene
    slot        2 = Paul
    slot        3 = -
    slot        4 = Paula
    slot        5 = Harry
    slot        6 = Dirk
    slot        7 = -
    slot        8 = -
    slot        9 = Dianna
    slot       10 = Bobby
    n_slots = 11
    n_items in table = 8
    Load factor =  0.727
    <BLANKLINE>
    >>> 'Harry' in hash_table
    True
    >>> 'Paul' in hash_table
    True
    >>> 'Paula' in hash_table
    True
    >>> 'David' in hash_table
    True
    >>> 'Bobby' in hash_table
    True
    >>> 'Dianna' in hash_table
    True
    >>> 'Dirk' in hash_table
    True
    >>> 'Darlene' in hash_table
    True
    >>> 'Dingus' in hash_table
    False
    >>> hash_table2 = QuadraticHashTable(7)
    >>> hash_table2.store('Tee')
    >>> hash_table2.store('Aby')
    >>> hash_table2.store('Ken')
    >>> hash_table2.store('Fin')
    >>> hash_table2.store('Sal')
    >>> print(hash_table2)
    QuadraticOpenAddressHashTable:
    slot        0 = -
    slot        1 = Sal
    slot        2 = Aby
    slot        3 = Ken
    slot        4 = Tee
    slot        5 = Fin
    slot        6 = -
    n_slots = 7
    n_items in table = 5
    Load factor =  0.714
    <BLANKLINE>
    >>> print('Sal' in hash_table2)
    True
    """

    def __init__(self, slots=11):
        """
        Creates a new hashtable with a number of slots (default: 11).
        Remember we can't have a load factor greater than 1 for an open hash...
        Note:
        Your hash table should stay at the initial size, that is, you are not
        expected to resize the hash table if it becomes overful. This will
        just create an error.
        """
        self._data = [None for i in range(slots)]
        self.n_slots = slots
        self.n_items = 0

    def _hash(self, item):
        """Return the hash of an item.
        First calculate using nice_hash(item) and then use modulo
        to reduce it down to a number in the range 0..self.n_slots
        """
        return nice_hash(item) % self.n_slots

    def _next_free_slot(self, first_hash):
        """
        Keeps incrementing hash index until an empty slot is found.
        Then returns the index of that slot.
        Used by the store method to help deal with a collisions.
        Note: this method isn't useful in __contains__ but you should
              follow a similar series of probing there.
        """
        curr_index = first_hash
        try_number = 0
        tried = []
        # print self._data
        while self._data[curr_index] is not None:
            tried.append(curr_index)
            try_number += 1
            if try_number > self.n_slots // 2:
                # print self._data
                print('Size = ' + str(self.n_slots))
                print('Number of items = ' + str(self.n_items))
                print('Failed to find an empty slot...')
                print('Try number = ' + str(try_number))
                print('List of tried slots = ' + str(tried))
                print('Current table = ' + str(self._data))
                print('*** Failed to find an empty slot!!!! ')
                print('*** This can happen with quadratic probing')
                print('*** if the table is over half full')
                raise ValueError('Failed to find an empty slot!!!!')
            else:
                curr_index = (first_hash + try_number**2) % self.n_slots
        return curr_index

    def store(self, item):
        """Stores an item in the hashtable.
        Notes:
            - self._next_free_slot will sometimes be handy here...
            - once a quadratic probing hash table is over half
              full we can't guarantee an empty slot will be found!
        """
        if self.n_slots == self.n_items:
            # Argh - crash, who made the hashtable too small?
            # Note - students aren't expected to resize the hash table,
            #       simply raising an error is fine.
            print(self._data)
            print('Size = ' + str(self.n_slots))
            print('Slots used = ' + str(self.n_items))
            print("Hash table is full!!!! You eeediot")
            print("A good Hasher would have resized the hash table by now!")
            raise ValueError("Hash table is full!!!!")
        # **************************************************
        # ---start student section---
        current_slot = self._hash(item)
        if self._data[current_slot] is None:
            self._data[current_slot] = item
        else:
            current_slot = self._next_free_slot(current_slot)
            self._data[current_slot] = item
        # ===end student section===
        self.n_items += 1

    def __contains__(self, item):
        """
        Checks to see if an item is stored within the hashtable.
        Returns True if it is, otherwise it returns False.
        Note: The function should give up and return False if
        the try_number reaches the number of slots in the table.
        At this stage we definitely know we are in a never ending
        cycle and will never find the item...
        You can call this method using Python's 'in' keyword:
            ht = HashTable()
            ...
            if 'foo' in ht:
                ...
        """
        first_hash = self._hash(item)
        try_number = 0
        current_index = first_hash
        # ---start student section---
        while try_number < self.n_slots:
            if self._data[current_index] == item:
                return True
            try_number += 1
            current_index = (first_hash + try_number**2) % self.n_slots
        # ===end student section===

    def __str__(self):
        output = 'QuadraticOpenAddressHashTable:\n'
        for i in range(self.n_slots):
            output += f'slot {i:8} = '
            item = self._data[i]
            if item is None:
                output = output + '-'
            else:
                output = output + str(item)
            output += '\n'
        load_factor = float(self.n_items) / self.n_slots
        output += f'n_slots = {self.n_slots}\n'
        output += f'n_items in table = {self.n_items}\n'
        output += f'Load factor = {load_factor:6.3f}\n'
        return output

    def __repr__(self):
        return str(self)

# =====================================================================


def load_dict_words(filename):
    """
    Load a dictionary from a file, and returns a list of all words in the
    dictionary.
    Dictionary files should have one word per line.
    """
    with open(filename, 'r', encoding='latin_1') as file:
        words = [line.strip().lower() for line in file]
    return words


def load_doc_words(filename):
    """
    Loads a document from a file, and returns a list of all words in the
    document. 'Words' are sequences of one or more [A-Za-z] characters.
    Words are converted to lowercase.
    """
    with open(filename, 'r', encoding='ascii') as file:
        words = [word.lower()
                            for word in re.findall(r'[A-Za-z]+', file.read())]
    return words


# ---------------------------------------------------------------------------------------
def spellcheck_with_list(
    document_word_list,
    dictionary_word_list,
     quiet_mode=False):
    """
    Checks the spelling of each word in document_word_list (a list of words from a text)
    against the dictionary_word_list (the list of correct words).
    """
    # Check all words in the document_word_list list
    # Printing out misspelled words and counting them
    if not quiet_mode:
        print_line()
        print('Misspelled words:')
        print_line()

    # ***********************************************************
    # Write your spell check code below
    dictionary_length = len(dictionary_word_list)
    document_length = len(document_word_list)
    num_errors = 0
    unique_errors = set()  # hint hint :)
    start_check_time = perf_counter()
    # start
    for word in document_word_list:
        if word not in dictionary_word_list:
            num_errors += 1
            unique_errors.add(word)
    # end
    end_check_time = perf_counter()
    for i, word in enumerate(unique_errors):
        if not quiet_mode:
            print(f"{i+1:4d}: {word}")
    check_time = end_check_time - start_check_time
    ms_per_word = (check_time / len(document_word_list)) * 1000
    if not quiet_mode:
        print_line()
        print(f'Number of errors = {num_errors} words')
        print(f'Number of unique errors = {len(unique_errors)} words')
        print_line()
        print()
        print_line()
        print('Summary stats (using simple linear search):')
        print_line()
        print(f'Words in dictionary = {dictionary_length} words')
        print(f'Document length = {document_length} words')
        print(f'Document check time = {check_time:8.4f}s')
        print(f'Check time per word in document = {ms_per_word:10.6f} ms')
        print_line()
        print()

    return check_time


# ----------------------------------------------------------------------------
def build_hash_table(ht_type, ht_size, dictionary_word_list, quiet_mode=False):
    """ Stores all the dictionary words in a hash table of the
    given type and size.
    Returns the hash table and the time taken to build it
    """
    # Build Hash Table by adding words from the dictionary word list
    start_build_time = perf_counter()
    if ht_type == 'Chaining':
        hash_table = ChainingHashTable(ht_size)
    elif ht_type == 'Linear':
        hash_table = LinearHashTable(ht_size)
    elif ht_type == 'Quadratic':
        hash_table = QuadraticHashTable(ht_size)
    else:
        print('Hash type must be Chaining, Linear or Quadratic.')
    for word in dictionary_word_list:
        hash_table.store(word)
    end_build_time = perf_counter()
    build_time = end_build_time - start_build_time
    return hash_table, build_time


# ----------------------------------------------------------------------------
def spellcheck_with_hashtable(document_word_list,
                              dictionary_word_list,
                              ht_type,
                              ht_size,
                              quiet_mode=False):
    """
    Checks the spelling of each word in 'document' (a list of words) against
    the dictionary (another list of words, using the given hash_table).
    """
    hash_table, build_time = build_hash_table(
        ht_type, ht_size, dictionary_word_list)

    # Check all words in the document list
    # Printing out misspelled words and counting them
    if not quiet_mode:
        print_line()
        print('Misspelled words:')
        print_line()

    # Write your spell check code below
    # ***********************************************************
    dictionary_length = len(dictionary_word_list)
    document_length = len(document_word_list)
    unique_errors = set()  # hint hint :)
    num_errors = 0
    # ---- start -----
    start_check_time = perf_counter()
    for word in document_word_list:
        if word not in hash_table:
            num_errors += 1
            unique_errors.add(word)
    end_check_time = perf_counter()

    for i, word in enumerate(unique_errors):
        if not quiet_mode:
            print(f"{i+1:4d}: {word}")

    # ---- end ----
    check_time = end_check_time - start_check_time
    load_factor = float(hash_table.n_items) / hash_table.n_slots
    ms_per_word = (check_time / len(document_word_list)) * 1000
    if not quiet_mode:
        print_line()
        print(f'Number of errors = {num_errors} words')
        print(f'Number of unique errors = {len(unique_errors)} words')
        print_line()
        print()
        print_line()
        print('Summary stats (using ' + ht_type + ' hash table):')
        print_line()
        print(f'Words in dictionary = {dictionary_length} words')
        print('Hash table size = {0:d} slots'.format(hash_table.n_slots))
        print('Hash table load factor = {0:8.4f}'.format(load_factor))
        print('Hash table build time = {0:8.4f}s'.format(build_time))
        print(f'Document length = {document_length} words')
        print(f'Document check time = {check_time:8.4f}s')
        print(f'Check time per word in document = {ms_per_word:10.6f} ms')
        print_line()
        print()
    return check_time


def binary_search(values, needle):
    lowerBound = 0
    upperBound = len(values)
    index = 0
    # ---start student section---
    pass
    # ===end student section===
    return False


# ------------------------------------------------
def spellcheck_bin(document_word_list, dictionary_word_list, quiet_mode=False):
    # Check all words in the document list
    # Printing out misspelled words and counting them
    if not quiet_mode:
        print_line()
        print('Misspelled words:')
        print_line()
    num_errors = 0

    dict_sort_start = perf_counter()
    dictionary = sorted(dictionary_word_list)
    dict_sort_end = perf_counter()

    dictionary_length = len(dictionary_word_list)
    document_length = len(document_word_list)
    unique_errors = set()  # hint hint :)
    num_errors = 0

    # ---start student section---
    pass
    # ===end student section===
    if not quiet_mode:
        print_line()
        print(f'Number of errors = {num_errors} words')
        print(f'Number of unique errors = {len(unique_errors)} words')
        print_line()
        print()
        print_line()
        print('Summary stats (using Binary Search on Dictionary):')
        print_line()
        print(f'Words in dictionary = {dictionary_length} words')
        print(f'Time to sort dictionary = {dict_sort_time:.4f} ms')
        print(f'Document length = {document_length} words')
        print(f'Document check time = {check_time:8.4f}s')
        print(f'Check time per word in document = {ms_per_word:10.6f} ms')
        print_line()
        print()
    return check_time


if __name__ == '__main__':
    # you don't need to worry about what the next line does :)
    os.environ['TERM'] = 'linux'  # Suppress ^[[?1034h to keep doctests happy

    # change to True to get more doctest output
    with_verbose = False

    # When with_verbose is False you will get no output if all tests in the module pass
    # uncomment the next few lines when you are ready to run all the tests
    # result = doctest.testmod()
    # if with_verbose:
        # print(result)

    # Individual tests:
    # doctest.run_docstring_examples(
    # ChainingHashTable, None, verbose=with_verbose)
    # doctest.run_docstring_examples(LinearHashTable, None, verbose=with_verbose)
    doctest.run_docstring_examples(QuadraticHashTable, None, verbose=with_verbose)

    # run all the doctests:
    # doctest.testmod()

    # NOTE:
    # Use tester.py to do some test runs with hash tables and
    # to do some spellchecks on various files
