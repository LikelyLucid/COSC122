import time
import random
from quicksort import *
from matplotlib import pyplot
import sys

# Get the time units given by the perf_counter
# Note: time.clock has been deprecated in Python 3.3
# and replaced with the more precise perf_counter method

# define time.get_time to be the appropriate time counter
if sys.version_info < (3, 3):
    get_time = time.clock
    print('Using time.clock for timing - Python ver < 3.3')
else:
    get_time = time.perf_counter
    print('Using time.perf_counter for timing - Python ver >= 3.3')
    REZ = time.get_clock_info('perf_counter').resolution
    print('One unit of time is ' + str(REZ) + ' seconds')


def times_vs_size(list_of_ns, n_trials=50, pivot_type=LEFT_PIVOT):
    """ returns a list of average times for each of the ns in  list_of_ns """
    avg_times = []
    # we will run the testing for each give data size
    for n in list_of_ns:
        total_time = 0
        # run the sort many times and take the average time
        # to get the average sum the time across all trials
        # then divide by the number of trials
        for i in range(n_trials):
            numbers_to_sort = list(range(n))  # a sorted list
            # randomise the numbers_to_sort here if you want to test random data
            start = get_time()
            s = quicksort(numbers_to_sort, pivot_type)
            end = get_time()
            time_taken = end - start
            total_time += time_taken
        avg_time = total_time / n_trials
        # print(n, avg_time)  # see what's happening
        avg_times.append(avg_time)
    return avg_times


# You don't need to graph anything to answer the lab quiz questions
# But it's always fun to visualise what is going on
# If you want to get the average time for just one data size
# you could make the list_of_ns a list with just one number
# for example list_of_ns = [760] :)

# n is used to denote how many key values are to be sorted
# list_of_ns is a list of the size of lists to time sorting
# initially [40, 80, 120 ... 760]
# list_of_ns will be used as the x-axis on your graphs
# and average time will be plotted on the y-axis
list_of_ns = list(range(40, 800, 40))

# some quick and dirty plotting
n_trials = 50
avg_times = times_vs_size(list_of_ns, n_trials, pivot_type=LEFT_PIVOT)
axes = pyplot.axes()
# axes.plot(list_of_ns, avg_times, marker='o', color='blue')
axes.plot(list_of_ns, avg_times, marker='o', color='indigo')
axes.set_title(f'Time vs. List size, average of {n_trials} trials')
axes.set_xlabel('n')
axes.set_ylabel('Average Time per sort')
pyplot.show()


# to add more lines to the plot simply make more calls to plot
# eg,
# axes.plot(list_of_ns, avg_times, marker='o', color='indigo')
# axes.plot(list_of_ns, other_avg_times, marker='x', color='red')
