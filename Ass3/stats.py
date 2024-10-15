""" 
Used to help you check your comparisons count matches the actual number
of comparisons made between Name objects.

IMPORTANT - You shouldn't refer to _stats_, get_count in the answer you submit 
to the quiz server. They won't be available!
"""


# Set marking mode to False for testing
# NOTE: it will be set to True on the quiz server!
IS_MARKING_MODE = False
ERROR = "You can't use the stats in marking mode!"

NAME_COMPS = 'name_comparisons'
HASH_TABLES_CREATED = 'hash_tables_created'


class StatCounter:
    """ Used to help you check your comparison count
    You shouldn't use this in your answer code as it won't work!
    """

    if not IS_MARKING_MODE:
        _stats = {NAME_COMPS: 0, HASH_TABLES_CREATED: 0}
        _locks = {NAME_COMPS: False, HASH_TABLES_CREATED: False}
    else:
        _stats = {NAME_COMPS: ERROR, HASH_TABLES_CREATED: ERROR}
        _locks = {NAME_COMPS: ERROR, HASH_TABLES_CREATED: ERROR}

    def __init__(self, *args, **kwargs):
        raise TypeError("The StatCounter class should never be initialized!")

    @classmethod
    def increment(cls, counter):
        if not IS_MARKING_MODE:
            if not cls._locks[counter]:
                cls._stats[counter] += 1
        else:
            cls._stats[counter] = ERROR

    @classmethod
    def get_count(cls, counter):
        if not IS_MARKING_MODE:
            return cls._stats[counter]
        else:
            # you shouldn't be using this in your final code!
            raise ValueError(ERROR)

    @classmethod
    def set_count(cls, counter, count):
        if not IS_MARKING_MODE:
            if not cls._locks[counter]:
                cls._stats[counter] = count
        else:
            # you shouldn't be using this in your final code!
            raise ValueError(ERROR)

    @classmethod
    def reset_counts(cls):
        """ Resets all counters.
            Always works, even when locked """
        if not IS_MARKING_MODE:
            for item in cls._stats:
                cls._stats[item] = 0
        else:
            for item in cls._stats:
                cls._stats[item] = ERROR

    @classmethod
    def reset_count(cls, counter):
        """ Resets the count for just the given counter.
            Works even when locked
        """
        if not IS_MARKING_MODE:
            cls._stats[counter] = 0
        else:
            # you shouldn't be using this in your final code!
            cls._stats[counter] = ERROR

    @classmethod
    def lock_counter(cls, counter):
        """ Marking mode lock on counter """
        if not IS_MARKING_MODE:
            cls._locks[counter] = True
        else:
            # you shouldn't be using this in your final code!
            raise ValueError(ERROR)

    @classmethod
    def unlock_counter(cls, counter):
        """ Marking mode unlock on counter """
        if not IS_MARKING_MODE:
            cls._locks[counter] = False
        else:
            raise ValueError(ERROR)

