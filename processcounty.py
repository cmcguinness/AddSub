"""
    This does the bulk of the work of processing an individual county's changes
    in voter registration.

    Copyright 2016 Charles McGuinness
    This project is available in a CC Attribution license for you to use as you see fit.
    See README.md for details

"""

import csv
from typing import List

import filter
import metadata

changecount = 0

def doRecord(row, filters: List[filter.Filter]):
    for f in filters:
        f.voter(row)


def doNew(row, filters: List[filter.Filter]):
    for f in filters:
        f.addVoter(row)


def doDel(row, filters):
    for f in filters:
        f.delVoter(row)


def doChange(row1, row2, filters):
    for f in filters:
        f.changeVoter(row1, row2)


# The same voter can exist in two files, but something about them has changed.
#   At the moment, the only meaningful change we track is did they switch parties?
#   But others can be found...

party_index = metadata.get_column_index('Party')  # Only do this once, please...


def testMeaningfulChangeInRegistration(row1, row2):
    '''
    Did the registration change in a way that we're interested in?

    Currently, only a change in party is interesting...
    '''
    global party_index
    global changecount

    if row1[party_index] != row2[party_index]:
        # print("{},{},{} {}->{}".format(row1[1], row1[2], row1[4], row1[23], row2[23]))
        # changecount += 1
        return True

    return False


def compare_files(name1, name2, filters: List[filter.Filter]):
    file1 = open(name1, "r")
    file2 = open(name2, "r")

    reader1 = csv.reader(file1, delimiter='\t')
    reader2 = csv.reader(file2, delimiter='\t')

    rows1 = []
    rows2 = []

    for r in reader1:
        rows1.append(r)

    for r in reader2:
        rows2.append(r)

    # Upon a superficial inspection, it would appear that the voter files are sorted
    # by voter id.  But they are not quite.  Since the code requires the data in sorted
    # order, we have to sort it ourselves.

    #   We want to sort on the voter id...
    def key_func(x):
        return int(x[1])

    rows1.sort(key=key_func)
    rows2.sort(key=key_func)

    # Get the iterator over the rows...
    iter1 = iter(rows1)
    iter2 = iter(rows2)

    # These track our end of file conditions
    done1 = False
    done2 = False

    # Loop through all the voters in both lists....

    # This code seems kind of convoluted, but since the two files are mostly, but not completely
    # the same, we cannot proceed through them both in perfect lockstep. Instead, we need to proceed
    # through both files independently, pairing off matching rows and detecting where there
    # are additions or subtractions from the list

    # We prime the pump with the first row from each file (we assume there is such a row)
    row1 = next(iter1)
    row2 = next(iter2)

    # Update the general statistics about the first row from the "new" file...
    doRecord(row2, filters)

    # And away we go!
    while not (done1 or done2):

        # Do we have the same person in each file?
        if row1[1] == row2[1]:

            # Did they change in some significant way?
            if testMeaningfulChangeInRegistration(row1, row2):
                # If so, note the change...
                doChange(row1, row2, filters)

            # Move on to the next voter in each file...
            try:
                row1 = next(iter1)
            except StopIteration:
                done1 = True

            try:
                row2 = next(iter2)
                doRecord(row2, filters)
            except StopIteration:
                done2 = True

            continue

        # Is the voter in the "old" file not present in the "new" file?  We know this because the voter id
        # in the new file has advanced beyond the voter id in the old file (that is, it is greater than)

        # If this is missing voter, handle the subtraction...
        if row1[1] < row2[1]:
            doDel(row1, filters)

            try:
                row1 = next(iter1)
            except StopIteration:
                done1 = True

        # Else: The voter is present in the new file, but not in the old file, so this is
        # an addition to the voter rolls
        else:
            doNew(row2, filters)

            try:
                row2 = next(iter2)
                doRecord(row2, filters)

            except StopIteration:
                done2 = True

    # End of while loop

    # At this point, we have exhausted one or both of the voter files.
    # If not both, we need to process the stragglers who are either additions or subtractions
    # depending upon which file has left over rows

    # Are there some people at the end of the old list who are missing?
    if not done1:
        while not done1:
            doDel(row1, filters)

            try:
                row1 = next(iter1)
            except StopIteration:
                done1 = True

    # Are there some people at the end of the new list who are new?
    elif not done2:
        while not done2:
            try:
                row2 = next(iter2)
                doRecord(row2, filters)
                doNew(row2, filters)
            except StopIteration:
                done2 = True

    # global changecount
    # print("A total of {} people changed party".format(changecount))
    # changecount = 0
    return  # Not needed, but nice to know where the end of this mess is!!
