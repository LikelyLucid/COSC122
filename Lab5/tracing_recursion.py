""" Try to predict what these functions
    will do before running them...
"""


def count(val):
    """ Predict what I'll do before you run me """
    if val <= 0:
        print(val)
    else:
        print(val)
        count(val -1)


def recount(val):
    """ Predict what I'll do before you run me """
    if val <= 0:
        print(val)
    else:
        recount(val -1)
        print(val)


def boggle(val):
    """ Predict what I'll do before you run me """
    if val <= 0:
        print(val)
    else:
        boggle(val -1)
        print(val)
        boggle(val -1)

count(5)
