# AddSub
* Detect additions and subtractions to Florida's state voter rolls.
* Compute demographic statistics on the changes
* Generate CSV output with results

## Overview
This simple set of code is designed to allow you to determine who has been added or
subtracted from Florida's voter rolls by comparing the full list from month to month.
But not just all voters, but voters in a variety of demographic groups.

The thing that makes this unique is its ability to analyze the intersectional nature
of voters.  Want to know how african-american
women have been added/removed from voting rolls? You can do that.  But to do that, the code
has to look at each voter and determine which category (that you have chosen) they fall into.

The list of categories is defined in main.py as the list of filters to use.  You can have
can abritrary number of filters with arbitrary complexity.   There are several examples given in the
code to get you started.

Do you wish for different / additional statistics that the filters support but do not know python?
Contact me on Twitter at [@SocialSeerCom](https://twitter.com/SocialSeerCom) and I'll see
what I can do for you.

### Where to get historical voter data
You can download historical sets of Florida voter lists from [here](http://flvoters.com/downloads.html).

The older rolls are conveniently in .zip files so you can download them all at once.  The recent ones
are not, and you will have to download them one at a time (or figure out how to automate them).

Put each month's data into a separate directory as this program relies on that structure to process
the data from each county.

## Misc.

* The program computes the number of people added and removed from the voter rolls.  To do this, it identifies
each voter whose registration status has changed from period to period. It would be quicker and easier to identify
the net changes just by aggregating the numbers, but that wouldn't give you the same sense
of volatility in the overall numbers.
* Since this does not track moves between counties, I suspect the #s it generates for both additions and
subtractions are higher than they really are; this seems to be confirmed by the fact that my numbers are consistently
higher than the #s given in the state's monthly report.
* I have no idea if this will work or how to make it work for other states.

### Todos:

* Detect changes in a record which isn't an addition or subtraction (e.g., party switch).  Right now,
these are just ignored.
* Detect people who have moved from one county to another.  Right now, they are treated as deletions
from one county and additions to another.


This is written in python version 3.5, and relies on some features present only in 3.5.
Only standard libraries are used at this point.

Copyright 2016 Charles McGuinness
This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

