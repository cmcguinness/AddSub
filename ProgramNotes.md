# Program Notes

This program is designed to perform statistical analysis of the changes between two dumps
of the Florida voter rolls.  Here is some high level information worth knowing:

The code is split into four files:

* main.py: This is the driver program.  If you wish to generate different statistics,
this is generally the place to start.
* filter.py: This is a class which allows you to create various filters. Filters have two purposes
(this should probably be refactored into two classes at some point).  The first purpose of a filter
is to determine whether or not a row matches the criteria for the filter.  For example, you could
define a filter which only looks for black males under the age of 30.  The second purpose of
a filter is to count how many voters match the filter, how many have been added, and how many have been
deleted.  The filter will count these both at the state-wide level as well as at the county level.
* processcounty.py: this module is used to process the voter rolls in a county.  It detects additions and subtractions
and applies the filters to them to generate the counts.
* metadata.py: This module basically just holds the metadata on the florida voter roll files -- what the names
for the columns are as well as the translation of the coded values back into english.


## Execution Overview
main.py starts the program off.  Here are the things to know about it:
* It has hard coded values for where to look for
the two sets of voter data as well as where to put the output, and you will want to change these.
* It calls myFilters()
to generate the list of filters (aka statistics) we want to generate.  You will want to change this list, as
well, to match your needs.
* Then the function doAnalysis() is called.  That function creates the output file, which is a tab-delimited format.
I have found that Excel handles tab-delimited much better than comma delimited, but if you wish to generate a
true CSV file, the change to the code is trivial.
* doAnalysis() then creates the header row from the list of filters.  Note that for each filter there is a total,
added, and deleted column.  The number of columns this program generates can grow very quickly.
* doAnalyis() enumerates and sorts the files in the two voter roll directories, and then loops over them,
feeding each matched pair to processcounty.py. After each county is processed, it generates a row in the output
file with the statistics for the county.
* Finally, doAnalysis() outputs a last row with the state-wide totals.

processcounty.py does the work of detectint the changes to a county's voter rolls.  Here's a few things to know about it:
* It reads both sets of data into memory, and the sorts on voter id.  This is so it
can efficiently detect additions and subtractions.
* It marches through the two voter lists, matching up voters from each.  When a voter appears in the old file
but not the new, it is considered a subtraction.  When a voter appears in the new file but not the old, it
it is considered an addition.
* Voters are matched on voter id only. If person changes their name or moves within a county, for example, this would be ignored.
* But I'm assuming that voter ids are not reused (or least not quickly enough to cause an issue for the code).

## Comments on design approach
There are two ways you could tackle looking at voter rolls.  The first, and probably the most common,
would be to just compute the aggregates on each month's files and compare the numbers.  For example, you could
count the number of democratic women in January and in February, and the difference between those two
numbers would tell you the net change between the months.

The second approach is to actually look at each voter and determine whether they've been added in the
new file, deleted, or they've changed in some interesting way (i.e., they've changed parties).  This is
a bit more complex, but not terribly so, and allows deeper insights into the data.  That's what this
program implements.

