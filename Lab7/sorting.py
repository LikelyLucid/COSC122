def load_file(filename):
    """ Reads integers from a file.
    The file should have one integer per line """
    return [int(line) for line in open(filename).read().splitlines()]


def selection_sort(file_name):
    """ Loads numbers from the given file and returns them as a sorted list.
    The numbers are sorted using selection sort - surprise, surprise!
    """
    alist = load_file(file_name)
    n_comps = 0
    for fill_slot in range(len(alist) -1, 0, -1):
        index_of_max = 0
        for location in range(1, fill_slot +1):
            if alist[location] > alist[index_of_max]:
                index_of_max = location
        # swap items in fill_slot and index_of_max - puts max into fill_slot
        alist[fill_slot], alist[index_of_max] = alist[index_of_max], alist[fill_slot]

    # Note: you will need to count the comparisons
    print('Selection sort on {}, {} items'.format(file_name, len(alist)))
    print('  Used {} comparisons.\n'.format(n_comps))
    return alist


def insertion_sort(file_name):
    """ Loads numbers from the given file and returns them as a sorted list.
    The numbers are sorted using insertion sort - surprise, surprise!
    """
    n_comps = 0
    alist = load_file(file_name)
    for index in range(1, len(alist)):
        stop = False
        currentvalue = alist[index]
        position = index
        while position > 0 and not stop:
            if alist[position -1] > currentvalue:
                alist[position] = alist[position -1]
                position = position - 1
            else:
                stop = True
        alist[position] = currentvalue

    # Note: you will need to count the comparisons
    print('Insertion sort on {}, {} items'.format(file_name, len(alist)))
    print('  Used {} comparisons.\n'.format(n_comps))
    return alist


def gap_insertion_sort(alist, start, gap):
    """
    In-place insertion sort on alist with given start and gap.
    Should return the number of key comparisons used.
      - students will need to insert code to count comparisons
      - hint, return the number of comparisons
    """
    for i in range (start +gap, len(alist), gap):
        currentvalue = alist[i]
        position = i
        stop = False
        while position >= gap and not (stop):
            if alist[position -gap] > currentvalue:
                alist[position] = alist[position - gap]
                position = position - gap
            else:
                stop = True
        alist[position] = currentvalue
    # Note: you will need to count the comparisons


def shell_sort(file_name):
    """
    Runs shell sort with gap starting at n//2 and then gap = gap //2 etc.
       - Students need to keep track of the total key comparisons used.
    """
    alist = load_file(file_name)
    gap = len(alist) // 2
    total_comparisons = 0
    gap_list = []
    while gap > 0:
        gap_list.append(gap)  # build a list of gaps used as we go
        for start_position in range(gap):
            gap_insertion_sort(alist, start_position, gap)
        gap = gap // 2
    # Note: you will need to count the comparisons
    print('Shell sort on {}, {} items, '.format(file_name, len(alist)))
    print('  Used {} comparisons.'.format(total_comparisons))
    print('    Gaps were {}\n'.format(gap_list))
    return alist


def shell_sort2(file_name, gap_list):
    """ Receives a list of gaps and runs shell sort with those gaps.
    If a gap is greater than the number of items then ignore and move to the next.
    Students need to:
       - complete the code for sorting. gap_insertion_sort is obviously still handy
       - Keep track of the total key comparisons used.
    """
    alist = load_file(file_name)
    total_comparisons = 0
    # ---start student section---
    pass
    # ===end student section===
    print(
    'Shellsort2 with gap list on {}, {} items'.format(
        file_name,
         len(alist)))
    print('  Used {}  comparisons.'.format(total_comparisons))
    print('    Gaps were {}: \n'.format(gap_list))
    return alist
