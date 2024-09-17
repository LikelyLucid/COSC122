'''Simple program for processing trace files to test arrays.'''
# Import all three classes so we can test them all
# Remember the sorted array won't count anything until you add your code
import sys
import time

from arrays import LinearArray, SortedArray, BitVectorArray

# NOTE: We recommend running in Python v3.8 or later to be consistent with
# lab machines.

# Get the time units given by the perf_counter
# Note: time.clock has been deprecated in Python 3.3
# and replaced with the more precise perf_counter method
# time.perf_counter returns time as seconds since some arbitrary time
# so only the difference between two times is useful...
REZ = time.get_clock_info('perf_counter').resolution
print('Smallest time resolution is ' + str(REZ) + ' seconds')


def process_file(filename, array):
    """
    Loads the array from a file. Files contain lines in the format:
        [instruction] [value]
    Valid instructions are:
        i : Insert [value]
        c : Contains [value]?
        d : Delete [value]
    [value] must be a valid positive integer.
    """
    file = open(filename)
    for i, line in enumerate(file):
        print(f'{i:>4}: ', end='')
        instruction, value = line.split(' ')
        value = int(value)
        if instruction == 'i':
            array.insert(value)
            print(f'{"insert":>10}{value:>5d}{array.comparisons:>8d} comparisons')
        elif instruction == 'c':
            print(f'{"contains":>10}{value:>5d}', end='')
            if array.contains(value):
                print(f'{array.comparisons:>8d} comparisons (found)')
            else:
                print(f'{array.comparisons:>8d} comparisons (not found)')
        elif instruction == 'd':
            array.remove(value)
            print(f'{"removed":>10}{value:>5d}{array.comparisons:>8d} comparisons')
        else:
            print('Whoops. Unknown command........')
    file.close()


def time_sorted_trial(filename):
    """ Times how long it takes to processes the
    given file with a SortedArray
    """
    test_array = SortedArray()
    print('\nRunning trial on sorted array with', filename)
    start_time = time.perf_counter()
    process_file(filename, test_array)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"Took {time_taken:.3f} seconds.")
    return time_taken


def time_linear_trial(filename):
    """ Times how long it takes to processes the
    given file with a LinearArray
    """
    test_array = LinearArray()
    print("\nRunning trial on sorted array with", filename)
    start_time = time.perf_counter()
    process_file(filename, test_array)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"Took {time_taken:.3f} seconds.")
    return time_taken

def time_bva_trial(filename, array_size):
    """ Times how long it takes to processes the
    given file with a BitVectorArray
    """
    test_array = BitVectorArray(array_size)
    print("\nRunning trial on sorted array with", filename)
    start_time = time.perf_counter()
    process_file(filename, test_array)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"Took {time_taken:.3f} seconds.")
    return time_taken


def main_tests():
    '''Do some file processing here...'''

    # # for example, process file0 with a LinearArray
    filename = 'file3.txt'
    # print('Processing', filename, 'with a linear array')
    # test_array = SortedArray()  # initialise a LinearArray
    # process_file(filename, test_array)
    # time_linear_trial(filename)
    time_sorted_trial(filename)

    # Add more tests here:)

    # call timing tests here when ready


if __name__ == '__main__':
    # This code won't run if this module is imported
    # It only runs if you run this module, eg, by hitting play in Wing
    main_tests()
