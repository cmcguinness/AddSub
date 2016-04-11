# AddSub
* Detect additions and subtractions to Florida's state voter rolls.
* Compute demographic statistics on the changes
* Generate CSV output with results

This simple set of code is designed to allow you to determine who has been added or
subtracted from Florida's voter rolls by comparing the full list from month to month.

There is a set of sample code that shows how you can also detect changes in a specific
party's registration or in a particular racial category.

Do you wish for different / additional statistics but do not know python?
Contact me on Twitter at [@SocialSeerCom](https://twitter.com/SocialSeerCom) and I'll see
what I can do for you.

You can download historical sets of Florida voter lists from [here](http://flvoters.com/downloads.html).

The older rolls are conveniently in .zip files so you can download them all at once.  The recent ones
are not, and you will have to download them one at a time (or figure out how to automate them).

Put each month's data into a separate directory as this program relies on that structure to process
the data from each county.

Notes:
* Since this does not track moves between counties, I suspect the #s it generates for both additions and
subtractions are higher than they really are; this seems to be confirmed by the fact that my numbers are consistently
higher than the #s given in the state's monthly report.
* I have no idea if this will work or how to make it work for other states.

This is written in python version 3.5.  Only standard libraries are used.

Copyright 2016 Charles McGuinness
This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

