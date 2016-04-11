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
import os

import metadata
import processcounty
from filter import Filter, OpEqual, OpNotIn


#   Define the filters we want to use
def myFilters():
    #   The filter structure is a bit complicated, but not too hard to understand.
    #
    #   A filter consists of two things:
    #
    #   1. The name (for use in generating the CSV output)
    #   2. The criteria (for identifying records that match)
    #
    #   The criteria is a list of zero or more rules.  All rules must be true for the filter to match
    #   (If there are zero rules, the rule matches by default)
    #
    #   Each rule has three parts:
    #
    #   1. The index in the record to look at. You can uses metadata.get_column_index() to
    #      translate nice english names into the numerical index needed for the rule
    #   2. The operator used for comparison: OpEqual, OpNotEqual, etc.
    #   3. What to compare against.  For most operators, it's a single value.  But for
    #      OpIn it's an arbitrarily long list.  For OpBetween, it's the lowest and highest value

    filters = []

    #   The simplest of all filters, one that admits all voters
    filters.append(Filter("All", []))

    #   Filters by party
    filters.append(Filter("Democrats", [[metadata.get_column_index("Party"), OpEqual, "DEM"]]))
    filters.append(Filter("Republicans", [[metadata.get_column_index("Party"), OpEqual, "REP"]]))
    filters.append(Filter("No Party", [[metadata.get_column_index("Party"), OpEqual, "NPA"]]))
    filters.append(Filter("Third Party", [[metadata.get_column_index("Party"), OpNotIn, ("DEM", "REP", "NPA")]]))

    #   Filters by race
    filters.append(Filter("Blacks", [[metadata.get_column_index("Race"), OpEqual, "3"]]))
    filters.append(Filter("Whites", [[metadata.get_column_index("Race"), OpEqual, "5"]]))
    filters.append(Filter("Other Races", [[metadata.get_column_index("Race"), OpNotIn, ("3", "5")]]))

    #   Filters by gender
    filters.append(Filter("Men", [[metadata.get_column_index("Gender"), OpEqual, "M"]]))
    filters.append(Filter("Women", [[metadata.get_column_index("Gender"), OpEqual, "F"]]))

    #   Example of a complex filter: African-American Women
    filters.append(Filter("Black Women", [
        [metadata.get_column_index("Race"), OpEqual, "3"],
        [metadata.get_column_index("Gender"), OpEqual, "F"]
    ]))

    return filters


#
#   Perform the actual analysis on the data
def doAnalysis(dir1, dir2, output_name, filters):
    output_file = open(output_name, "w")

    #   Print the header row of the data
    header = "County"

    for f in filters:
        header += "\t" + f.name + " Total"
        header += "\t" + f.name + " Added"
        header += "\t" + f.name + " Deleted"

    print(header, file=output_file)

    #   Find all the files in both directories to process.
    from_files = [f for f in os.listdir(dir1) if f.endswith(".txt")]
    to_files = [f for f in os.listdir(dir2) if f.endswith(".txt")]

    #   Sort the file names just to be sure they are in the same order
    from_files.sort()
    to_files.sort()

    for i in range(len(from_files)):
        print("Now processing {} county".format(metadata.county_name(from_files[i][0:3])))
        processcounty.compare_files(
            os.path.join(dir1, from_files[i]),
            os.path.join(dir2, to_files[i]),
            filters)

        line = metadata.county_name(from_files[i][0:3])
        for f in filters:
            line += "\t" + str(f.localTotal)
            line += "\t" + str(f.localAdditions)
            line += "\t" + str(f.localDeletions)
            f.resetLocal()

        print(line, file=output_file)
        output_file.flush()  # Not really necessary, but nice if you're monitoring the progress while this runs.

    line = "Florida"
    for f in filters:
        line += "\t" + str(f.globalTotal)
        line += "\t" + str(f.globalAdditions)
        line += "\t" + str(f.globalDeletions)

    print(line, file=output_file)

    output_file.close()


if __name__ == "__main__":
    #   Change these to the directories that hold your two sets of voter files.
    #   Unless you are also named Charles and are on a Mac, these values will not work for you...
    #   Files will be named in the format CountyCode_YYYYMMDD.txt

    dir1 = '/Users/charles/Projects/VoterFile/201512'
    dir2 = '/Users/charles/Projects/VoterFile/201601'

    # There is no reason, FWIW, you have to compare sequential months, although you might miss people
    # who come and go very quickly...

    # This is the name of the output file; it can be where ever you wish, but probably not here...
    output_name = '/Users/charles/Projects/VoterFile/Changes-2015-12-2016-01.txt'

    filters = myFilters()

    doAnalysis(dir1, dir2, output_name, filters)
