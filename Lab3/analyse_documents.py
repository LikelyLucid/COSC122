""" Calculates the frequencies of letters, letter paris, etc using
our linked frequency lists to keep track of the frequencies.
"""

from frequency_lists import *

# uncomment use the following import if you want to plot things!
# import matplotlib.pyplot as plt


def time_freq_build(doc, freq_list_class, n_chars):
    """Calculate the letter frequencies using the supplied freq_list_class and
    document (in the form of a string called doc).
    Returns a freq_list and the time_taken in seconds.
    """
    # create a new freq_list instance of the given class
    freq_list = freq_list_class()
    if n_chars == 1:
        # do a simple scan for single characters
        start = time.perf_counter()
        for char in doc:
            freq_list.add(char)
        end = time.perf_counter()
    elif n_chars > 1:
        # do a scan for given multiples of characters
        start = time.perf_counter()
        for i in range(0, len(doc) - n_chars):
            chars = doc[i : i + n_chars]
            freq_list.add(chars)
        end = time.perf_counter()
    else:
        raise ValueError("Number of characters must be a positive integer")
    time_taken = end - start
    return freq_list, time_taken


def plot_freq_list(freq_list):
    """Plots a bar chart showing item frequency.
    Will take any of the various freq_list classes, eg, unsorted, sorted etc
    NOTE: Remember to uncomment the matplotlib import at the start of the file
          if you are going to do some plotting
    """
    (xvals, yvals) = freq_list.get_xy_for_plot()
    item_list_nums = list(range(len(xvals)))
    width = 0.8
    fig, axes = plt.subplots()
    axes.bar(item_list_nums, yvals, width)
    axes.set_title("Frequency Distribution")
    axes.set_xlabel("Item")
    tick_positions = item_list_nums
    axes.set_xticks(tick_positions)
    axes.set_xticklabels(xvals)
    axes.set_ylabel("Frequencies")
    plt.show()


def plot_truncated_freq_list(freq_list, n_items=26):
    """Plots a bar chart showing item frequency for the first n items.
    Will take any of the various freq_list classes, eg, unsorted, sorted etc
    Note: If the frequency list is sorted then you'll see the n_items most
    frequent items. Otherwise you just see the first n_items in the list.
    NOTE: Remember to uncomment the matplotlib import at the start of the file
          if you are going to do some plotting
    """
    (raw_x, raw_y) = freq_list.get_xy_for_plot()
    # only use the first n items
    xvals = raw_x[:n_items]
    yvals = raw_y[:n_items]

    item_list_nums = list(range(len(xvals)))
    width = 0.8
    fig, axes = plt.subplots()
    axes.bar(item_list_nums, yvals, width)
    axes.set_title("Frequency Distribution (first " + str(n_items) + " items)")
    axes.set_xlabel("Item")
    tick_positions = item_list_nums
    axes.set_xticks(tick_positions)
    axes.set_xticklabels(xvals)
    axes.set_ylabel("Frequencies")
    plt.show()


def print_analysis_header(filename, doc_contents):
    """Does what it says."""
    print("\n" * 2)
    print("-" * 50)
    print("Frequency Analysis for: " + filename)
    print(f"Document size:  {len(doc_contents)} chars")
    print("-" * 50)


#############################################################################
# DO NOT MODIFY ANYTHING in this area
# ----------------------------------------------------------------------------
def format_document(input_doc):
    """Re-formats `input_doc` by collapsing all whitespace characters into a
    space and stripping all characters that aren't letters or punctuation.
    Converts all uppercase characters in the file to lower case.
    """
    # Collapse whitespace
    reduced_doc = re.compile(r"\s+", re.UNICODE).sub(" ", input_doc)
    # http://www.unicode.org/reports/tr44/#General_Category_Values
    allowed_categories = ("Lu", "Ll", "Lo", "Po", "Zs")
    formatted_doc = "".join(
        [c.lower() for c in reduced_doc if category(c) in allowed_categories]
    )
    return formatted_doc


######################## $$###################################################
#############################################################################


def analyse_document(doc_filename, freq_class, n_chars=1, verbose=True):
    """
    Loads and formats the contents in the file given by doc_filename.
    Calls the freq_list builder to calculate the frequencies
    of the n_char groups using the given freq_class.
    Then displays the how long it took.
    If verbose == True then prints out the resulting freq list.
    """

    with open(doc_filename, "r", encoding="utf-8") as infile:
        doc_contents = format_document(infile.read())
    print_analysis_header(doc_filename, doc_contents)

    # Time the building of the frequency list
    freq_list, total_time = time_freq_build(doc_contents, freq_class, n_chars)

    # Display time taken and frequency list if verbose
    n_items = len(freq_list)
    print(f"   {n_chars} char(s) -> t = {total_time:>.4f}s  ({n_items} items)")
    if verbose:
        print()
        print(freq_list)
        print("\n" * 4)  # leave 5 blank lines at the end

    # use something like the following for showing graphs
    # you will need matplotlib installed and
    # the import at the start of this file uncommented
    # plot_truncated_freq_list(freq_list, 10)
    # plot_freq_list(freq_list)


def main():
    """Gets the job done"""
    # Can enter an infinite loop if something isn't implemented correctly
    # So test on small data file first

    # **** Be sure to look at analyse_document to see how it works! ****
    # Uncomment the files you want to test
    # ------------------------------------

    # Some analyses using an UnsortedFreqList - add your own
    # analyse_document("ulysses.txt", UnsortedFreqList, n_chars=1, verbose=True)
    # analyse_document('ulysses.txt', UnsortedFreqList, n_chars=1, verbose=True)

    # some NicerUnsortedFreqList runs - add your own
    # analyse_document('le_rire.txt', NicerUnsortedFreqList, n_chars=1, verbose=True)
    # analyse_document('ulysses.txt', NicerUnsortedFreqList, n_chars=1, verbose=True)

    # some SortedFreqList runs - add your own
    # analyse_document('le_rire.txt', SortedFreqList, n_chars=2, verbose=True)
    # analyse_document('ulysses.txt', SortedFreqList, n_chars=2, verbose=True)
    analyse_document('war_and_peace.txt', SortedFreqList, n_chars=2, verbose=True)


if __name__ == "__main__":
    main()
