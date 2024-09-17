"""
Make sure you checkout all the helpful tests
that are commented out below so that you don't
have to re-write them yourself!!!
"""

from spelling import *

# test file names listed from smallest file to largest file
DOCS = ['sherlock.txt', 'trgov.txt', 'humnature.txt']


dictionary_word_list = load_dict_words("./Lab4/words_latin-1.txt")


doc_word_list = load_doc_words("./Lab4/"+DOCS[2])
# also try with other texts


# ---------------------------------------------------------------------
# Check with plain list = linear search
# ---------------------------------------------------------------------
# The spellcheck_with_list function will simply use
# the raw dicionary (ie the simple list of words in the dictionary) to do
# it's checking

# check_time = spellcheck_with_list(doc_word_list, dictionary_word_list)


# see http://www.bigprimes.net/archive/prime/
# for a big list of prime numbers
# prime sized hashtables can help modulo hashing spread hash values more evenly

sizes = [650011, 700001, 800011, 2000003, 3000017, 5000011, 10000019]

# doc_word_list = load_doc_words("./Lab4/" + DOCS[2])
# for size in sizes:
#     print(f"Size: {size}")
#     # check_time = spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Chaining', size)
#     check_time = spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Linear', size, quiet_mode=True)
#     print("Linear Hashable Time: ", check_time)
#     check_time = spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Quadratic', size, quiet_mode=True)
#     print("Quadratic Hashable Time: ", check_time)


    # check_time = spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Quadratic', size)
# ---------------------------------------------------------------------
# Check with various hashtable implementations and sizes
# ---------------------------------------------------------------------
# The spellcheck_with_hashtable will first put all
# the words in the dictionary into a hashtable
# then it will use the hashtable to lookup words
# in the given text

# check_time = spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Chaining', 11)
# check_time = spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Chaining', 800011)
# check_time = spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Linear', 2000003)
# check_time = spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Quadratic', 800011)

# feel free to do tests for multiple sizes and files,
# eg, for size in sizes:
#
# NOTE:
# Quiet mode doesn't print words while checking and doesn't print summary table.
# To make quiet mode work make sure you use the following in your checker code
#      if not quiet_mode: print(word)
# To use quiet mode, call with optional quiet_mode param, eg,
# spellcheck_with_hashtable(doc_word_list, dictionary_word_list, 'Quadratic', 800011, quiet_mode=True)

# ---------------------------------------------------------------------
# Check with binary search
# ---------------------------------------------------------------------
# spellcheck_bin(doc_word_list, dictionary_word_list)


# ---------------------------------------------------------------------
# See how various hashtables are filled
# ---------------------------------------------------------------------

# You can use print statements between store commands
# to see how the hashtable fills up.
# For example:
# hash_table = ChainingHashTable(5)
# hash_table.store('Paul')
# print(hash_table)
# hash_table.store('Peter')
# print(hash_table)
# hash_table.store('Paula')
# print(hash_table)
# hash_table.store('David')
# print(hash_table)
# hash_table.store('Bobby')
# print(hash_table)
# hash_table.store('Dianne')
# print(hash_table)


# hash_table = ChainingHashTable(5)
# hash_table.store('George')
# hash_table.store('Bungle')
# hash_table.store('Zippy')
# hash_table.store('Jane')
# hash_table.store('Rod')
# hash_table.store('Freddy')

# hash_table = ChainingHashTable(5)
# hash_table.store('Paul')
# hash_table.store('Peter')
# hash_table.store('Paula')
# hash_table.store('David')
# hash_table.store('Bob')
# hash_table.store('Di')
# print(hash_table)


# hash_table = LinearHashTable(7)
# hash_table.store('Tennis')
# print(hash_table)
# hash_table.store('Cricket')
# print(hash_table)
# hash_table.store('Swimming')
# print(hash_table)
# hash_table.store('Underwater Motorbike Hockey')
# print(hash_table)
# hash_table.store('Soccer')
# print(hash_table)

# hash_table = LinearHashTable(7)
# hash_table.store('Bob')
# hash_table.store('Zac')
# hash_table.store('Aby')
# hash_table.store('Kay')
# hash_table.store('Moe')
# print(hash_table)


# hash_table = LinearHashTable(7)
# hash_table.store('Aby')
# hash_table.store('Ken')
# hash_table.store('Nat')
# hash_table.store('Jim')
# print(hash_table)


# hash_table = LinearHashTable(7)
# hash_table.store('Nat')
# hash_table.store('Jam')
# hash_table.store('Aby')
# hash_table.store('Ren')
# print(hash_table)


# hash_table = LinearHashTable(7)
# hash_table.store('Moe')
# hash_table.store('Bob')
# hash_table.store('Zac')
# hash_table.store('Aby')
# hash_table.store('Kay')
# print(hash_table)


# hash_table = QuadraticHashTable(7)
# hash_table.store('Paul')
# print(hash_table)
# hash_table.store('Peter')
# print(hash_table)
# hash_table.store('Paula')
# print(hash_table)
# hash_table.store('David')
# print(hash_table)
# hash_table.store('Bobby')
# print(hash_table)
# hash_table.store('Dianna')
# print(hash_table)
# hash_table.store('Dick')
# print(hash_table)
# hash_table.store('Bob')
# print(hash_table)
# hash_table.store('Bart')
# print(hash_table)

# hash_table = QuadraticHashTable(7)
# hash_table.store('Aby')
# hash_table.store('Ken')
# hash_table.store('Nat')
# hash_table.store('Jim')
# hash_table.store('Bob')
# print(hash_table)


# hash_table = QuadraticHashTable(7)
# hash_table.store('Lee')
# hash_table.store('Aby')
# hash_table.store('Ken')
# hash_table.store('Nat')
# hash_table.store('Jim')
# print(hash_table)


hash_table = QuadraticHashTable(7)
hash_table.store('Jim')
hash_table.store('Aby')
hash_table.store('Ken')
hash_table.store('Bob')
hash_table.store('Art')
hash_table.store('Jon')
print(hash_table)


# hash_table = QuadraticHashTable(7)
# hash_table.store('Ron')
# hash_table.store('Jim')
# hash_table.store('Aby')
# hash_table.store('Ken')
# hash_table.store('Bob')
# hash_table.store('Art')
# print(hash_table)
