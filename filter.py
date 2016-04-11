OpEqual = 0
OpNotEqual = 1
OpIn = 2
OpNotIn = 3
OpBetween = 4  # Inclusive


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
    def __init__(self, name, criteria):
        self.name = name
        self.criteria = criteria
        self.globalTotal = 0
        self.localTotal = 0
        self.globalAdditions = 0
        self.localAdditions = 0
        self.globalDeletions = 0
        self.localDeletions = 0

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
            if c[1] == OpEqual:
                if row[c[0]] != c[2]:
                    return False
            elif c[1] == OpNotEqual:
                if row[c[0]] == c[2]:
                    return False
            elif c[1] == OpIn:
                if not row[c[0]] in c[2]:
                    return False
            elif c[1] == OpNotIn:
                if row[c[0]] in c[2]:
                    return False
            else:  # OpBetween
                if row[c[0]] < c[2][0]:
                    return False
                if row[c[0]] > c[2][0]:
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

    def resetLocal(self):
        self.localAdditions = 0
        self.localDeletions = 0
        self.localTotal = 0

    def getLocalStats(self):
        return (self.localTotal, self.localAdditions, self.localDeletions)

    def getGlobalStats(self):
        return (self.globalTotal, self.globalAdditions, self.globalDeletions)
