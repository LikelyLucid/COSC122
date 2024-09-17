def rec_list_print(alist, start_index=0):
    """ BIGN bONG """
    if start_index == len(alist):
        return
    print(alist[start_index])
    rec_list_print(alist, start_index + 1)
