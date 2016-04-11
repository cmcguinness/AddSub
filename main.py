"""
    Detect Changes to Florida's Voter Rolls

    Florida publishes a monthly extract of the voter rolls.  You can use this simplistic code to detect
    who has been added and who has been removed from the rolls. (It does not detect people who have
    moved between counties, however).

    The code also performs some simple statistics on the changes, allowing you to detect, for example,
    if there's been a disproportionate purge of african-american voters.

    Copyright 2016 Charles McGuinness
    This project is available in a CC Attribution license for you to use as you see fit.
    See README.md for details

"""
import csv
import os
import metadata


#   Change these to the directories that hold your two sets of voter files.
#   Unless you are also named Charles and are on a Mac, these values will not work for you...
#   Files will be named in the format CountyCode_YYYYMMDD.txt

dir1 = '/Users/charles/Projects/VoterFile/201512'
dir2 = '/Users/charles/Projects/VoterFile/201601'

# There is no reason, FWIW, you have to compare sequential months, although you might miss people
# who come and go very quickly...

# This is the name of the output file; it can be where ever you wish, but probably not here...
output_name = '/Users/charles/Projects/VoterFile/Changes-2015-12-2016-01.txt'

output_file = open(output_name, "w")

stateNew = 0
stateDropped = 0
stateTotal = 0
stateBlackDropped = 0
stateBlackTotal = 0
stateDemDropped = 0
stateDemTotal = 0


def compare_files(name1,name2,county):
    global stateNew
    global stateDropped
    global stateTotal
    global stateBlackDropped
    global stateDemDropped

    file1 = open(name1, "r")
    file2 = open(name2, "r")

    reader1 = csv.reader(file1, delimiter = '\t')
    reader2 = csv.reader(file2, delimiter = '\t')

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

    # These are our per county stats
    totalVoters = 0
    totalDropped = 0
    totalBlackDropped = 0
    totalBlack = 0
    totalDemDropped = 0
    totalDem = 0
    totalNew = 0

    # For each row in the "new" file, we want to calcualte some set of statistics
    # This function gets each row and will examine it to updates the appropriate counts....
    def updateDemo(row):
        nonlocal totalBlack
        nonlocal totalDem
        nonlocal totalVoters
        global stateBlackTotal
        global stateDemTotal
        global stateTotal

        totalVoters += 1
        stateTotal += 1

        if row[20] == '3':
            totalBlack += 1
            stateBlackTotal += 1

        if row[23] == 'DEM':
            totalDem += 1
            stateDemTotal += 1

    # This function processes the information about a voter who has been dropped from the rolls
    # You can change it to handle whatever demographic tracking you wish
    def missingVoter(row):
        nonlocal totalDropped
        nonlocal totalBlackDropped
        nonlocal totalDemDropped

        global stateBlackDropped
        global stateDemDropped
        global stateDropped

        totalDropped += 1
        stateDropped += 1

        if int(row1[20]) == 3:
            stateBlackDropped += 1
            totalBlackDropped += 1

        if row1[23] == 'DEM':
            totalDemDropped += 1
            stateDemDropped += 1

    # This function processes information about new voters.  So far, it just processes counts...
    def newVoter(row):
        nonlocal totalNew
        global stateNew
        totalNew += 1
        stateNew += 1


    # Loop through all the voters in both lists....

    # This code seems kind of convoluted, but since the two files are mostly, but not completely
    # the same, we cannot proceed through them both in perfect lockstep. Instead, we need to proceed
    # through both files independently, pairing off matching rows and detecting where there
    # are additions or subtractions from the list

    # We prime the pump with the first row from each file (we assume there is such a row)
    row1 = next(iter1)
    row2 = next(iter2)

    # Update the general statistics about the first row from the "new" file...
    updateDemo(row2)

    # And away we go!
    while not (done1 or done2):

        # Do we have the same person in each file?
        if row1[1] == row2[1]:
            # If so, then neither an addition nor a subtraction.
            # Move on to the next voter in each file...
            try:
                row1 = next(iter1)
            except StopIteration:
                done1 = True

            try:
                row2 = next(iter2)
                updateDemo(row2)        # This is subtle but important -- update the demos as we read in new voters
            except StopIteration:
                done2 = True

            continue

        # Is the voter in the "old" file not present in the "new" file?  We know this because the voter id
        # in the new file has advanced beyond the voter id in the old file (that is, it is greater than)

        # If this is missing voter, handle the subtraction...
        if row1[1] < row2[1]:
            missingVoter(row1)

            try:
                row1 = next(iter1)
            except StopIteration:
                done1 = True

        # Else: The voter is present in the new file, but not in the old file, so this is
        # an addition to the voter rolls
        else:
            newVoter(row2)

            try:
                row2 = next(iter2)
                updateDemo(row2)       # This is subtle but important -- update the demos as we read in new voters
            except StopIteration:
                done2 = True

    # End of while loop

    # At this point, we have exhausted one or both of the voter files.
    # If not both, we need to process the stragglers who are either additions or subtractions
    # depending upon which file has left over rows

    # Are there some people at the end of the old list who are missing?
    if not done1:
        while not done1:
            missingVoter(row1)

            try:
                row1 = next(iter1)
            except StopIteration:
                done1 = True

    # Are there some people at the end of the new list who are new?
    elif not done2:
        while not done2:
            try:
                row2 = next(iter2)
                updateDemo(row2)
                newVoter(row2)
            except StopIteration:
                done2 = True

    print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(county, totalVoters, totalNew, totalDropped, totalDem, totalDemDropped, totalBlack, totalBlackDropped), file=output_file)

    return      # Not needed, but nice to know where the end of this mess is!!


#   This is the "main" part of the code:

#   Print the header row of the data
print("County\tTotal\tNew\tDropped\tDemocracts\tDemocrats Dropped\tBlacks\tBlacks Dropped", file=output_file)

#   Find all the files in both directories to process.
from_files = [f for f in os.listdir(dir1) if f.endswith(".txt")]
to_files = [f for f in os.listdir(dir2) if f.endswith(".txt")]

#   Sort the file names just to be sure they are in the same order
from_files.sort()
to_files.sort()

for i in range(len(from_files)):
    print("Now processing {} county".format(metadata.county_name(from_files[i][0:3])))
    compare_files(os.path.join(dir1, from_files[i]),
                  os.path.join(dir2, to_files[i]),
                  metadata.county_name(from_files[i][0:3]))
    output_file.flush()     # Not really necessary, but nice if you're monitoring the progress while this runs.

print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format('Florida', stateTotal, stateNew, stateDropped, stateDemTotal, stateDemDropped, stateBlackTotal, stateBlackDropped), file=output_file)
