import datetime

#   Operators for use in filters
OpEqual = 0
OpNotEqual = 1
OpIn = 2
OpNotIn = 3
OpBetween = 4  # Inclusive
OpChangedFromTo = 5

#   Derived Columns
derivedAge = -1



class Filter:
    """
        A Filter is an object that track registrations for a specific set of criteria
        It allows you to define the criteria to match, and then will note the total number
        of records that match, the number of deletions and the number of additions.

        In addition, it will compute grand totals as well as county level subtotals.

    """

    #   Instance creation:
    #       name: The name to refer to this as
    #       criteria: an n-tuple of 2-tuples that defines what to look for.
    #       trackchange: also keep track of changes into or out of this criteria (party changes)
    #       ischange: only track the specific change in the criteria
    def __init__(self, name, criteria, trackchange=False, ischange=False):
        self.name = name
        self.criteria = criteria
        self.globalTotal = 0
        self.localTotal = 0
        self.globalAdditions = 0
        self.localAdditions = 0
        self.globalDeletions = 0
        self.localDeletions = 0
        self.localChangeOut = 0
        self.localChangeIn = 0
        self.globalChangeOut = 0
        self.globalChangeIn = 0
        self.trackchanges = trackchange
        self.ischange = ischange

    #   Compute Value of a Derived Column
    #
    #   So far, only supports age in years...
    def computeValue(self, row, index):
        if index == derivedAge:
            birthdate = row[21]  # MAGIC DEPENDENCY....
            try:
                born = datetime.datetime.strptime(birthdate, '%m/%d/%Y')
            except ValueError:
                return None

            today = datetime.date.today()
            years = today.year - born.year
            if today.month < born.month:
                years -= 1
            elif today.month == born.month and today.day < born.day:
                years -= 1

            return years

        return None





    #
    #   Criteria matching:
    #
    #   The criteria passed in as part of the object creation is a tuple (or list)
    #   where each element is, itself, a tuple with three elements.  The first
    #   element is an index into the voter record (e.g., 20 is Race; see the metadata).
    #   The second element is the operator used to compare the values
    #   The third is the value (or values) it must match.
    #
    #   All criteria elements much match
    #
    #   An empty criteria list matches all records.
    #
    #   Argument: row, a row from the voter data
    #   Returns: True/False, if the criteria matches


    def matchesCriteria(self, row):
        for c in self.criteria:
            if c[0] >= 0:
                column = row[c[0]]
            else:
                column = self.computeValue(row, c[0])

            if column is None:
                return False

            if c[1] == OpEqual:
                if column != c[2]:
                    return False
            elif c[1] == OpNotEqual:
                if column == c[2]:
                    return False
            elif c[1] == OpIn:
                if not column in c[2]:
                    return False
            elif c[1] == OpNotIn:
                if column in c[2]:
                    return False
            elif c[1] == OpChangedFromTo:
                return False  # These rules operate between registrations
            else:  # OpBetween
                if column < c[2][0]:
                    return False
                if column > c[2][1]:
                    return False

        return True

    #   Compute basis statistics for a voter
    def voter(self, row):
        if self.matchesCriteria(row):
            self.globalTotal += 1
            self.localTotal += 1

    def addVoter(self, row):
        if self.matchesCriteria(row):
            self.globalAdditions += 1
            self.localAdditions += 1

    def delVoter(self, row):
        if self.matchesCriteria(row):
            self.globalDeletions += 1
            self.localDeletions += 1

    def changeVoter(self, oldRow, newRow):
        if self.trackchanges:
            oldMatches = self.matchesCriteria(oldRow)
            newMatches = self.matchesCriteria(newRow)

            if oldMatches and not newMatches:
                self.localChangeOut += 1
                self.globalChangeOut += 1

            if newMatches and not oldMatches:
                self.localChangeIn += 1
                self.globalChangeIn += 1

        if self.ischange:
            c = self.criteria[0]
            if c[1] == OpChangedFromTo:
                if oldRow[c[0]] == c[2][0] and newRow[c[0]] == c[2][1]:
                    self.localTotal += 1
                    self.globalTotal += 1



    def resetLocal(self):
        self.localAdditions = 0
        self.localDeletions = 0
        self.localTotal = 0
        self.localChangeIn = 0
        self.localChangeOut = 0

        # def getLocalStats(self):
        #     return (self.localTotal, self.localAdditions, self.localDeletions)
        #
        # def getGlobalStats(self):
        #     return (self.globalTotal, self.globalAdditions, self.globalDeletions)
