"""

    Voter File Metadata definitions

    This is a fairly straightforward rendering of the information in the
    voter file layout documentation.

    Copyright 2016 Charles McGuinness
    This project is available in a CC Attribution license for you to use as you see fit.
    See README.md for details

"""
import filter

#   The columns in the voter extract file
voter_columns = []
voter_columns.append("County")
voter_columns.append("Voter ID")
voter_columns.append("Last")
voter_columns.append("Suffix")
voter_columns.append("First")
voter_columns.append("Middle")
voter_columns.append("Public Records Exemption")
voter_columns.append("Residence Address 1")
voter_columns.append("Residence Address 2")
voter_columns.append("Residence City")
voter_columns.append("Residence State")
voter_columns.append("Residence Zip")
voter_columns.append("Mailing Address 1")
voter_columns.append("Mailing Address 2")
voter_columns.append("Mailing Address 3")
voter_columns.append("Mailing City")
voter_columns.append("Mailing State")
voter_columns.append("Mailing Zip")
voter_columns.append("Mailing Country")
voter_columns.append("Gender")
voter_columns.append("Race")
voter_columns.append("Birth Date")  # Not that filter "knows" this is 21.  Change if this changes
voter_columns.append("Registration date")
voter_columns.append("Party")
voter_columns.append("Precinct")
voter_columns.append("Precinct Group")
voter_columns.append("Precinct Split")
voter_columns.append("Precinct Suffix")
voter_columns.append("Voter Status")
voter_columns.append("Congress District")
voter_columns.append("House District")
voter_columns.append("Senate District")
voter_columns.append("County Commission District")
voter_columns.append("School District")
voter_columns.append("Daytime Area Code")
voter_columns.append("Daytime Phone Number")
voter_columns.append("Daytime Phone Extension")
voter_columns.append("Email address")

#   Derrived columns are statistics which are computed from the actual data in the file.
voter_derived_columns = dict()
voter_derived_columns['Age'] = filter.derivedAge  # Voter's age in years



def get_column_index(name):
    for i in range(len(voter_columns)):
        if voter_columns[i] == name:
            return i
    if name in voter_derived_columns:
        return voter_derived_columns[name]

    return -1



#   The three letter county codes
counties = dict()
counties["ALA"]="Alachua"
counties["DES"]="Desoto"
counties["BAK"]="Baker"
counties["GLA"]="Glades"
counties["BAY"]="Bay"
counties["HAR"]="Hardee"
counties["BRA"]="Bradford"
counties["HEN"]="Hendry"
counties["CAL"]="Calhoun"
counties["HIG"]="Highlands"
counties["CLA"]="Clay"
counties["HIL"]="Hillsborough"
counties["CLM"]="Columbia"
counties["LEE"]="Lee"
counties["DIX"]="Dixie"
counties["MAN"]="Manatee"
counties["DUV"]="Duval"
counties["PAS"]="Pasco"
counties["ESC"]="Escambia"
counties["PIN"]="Pinellas"
counties["FRA"]="Franklin"
counties["POL"]="Polk"
counties["GAD"]="Gadsden"
counties["SAR"]="Sarasota"
counties["GIL"]="Gilchrist"
counties["DAD"]="Miami-Dade"
counties["GUL"]="Gulf"
counties["MON"]="Monroe"
counties["HAM"]="Hamilton"
counties["BRO"]="Broward"
counties["HOL"]="Holmes"
counties["IND"]="Indian River"
counties["JAC"]="Jackson"
counties["MRT"]="Martin"
counties["JEF"]="Jefferson"
counties["OKE"]="Okeechobee"
counties["LAF"]="Lafayette"
counties["PAL"]="Palm Beach"
counties["LEO"]="Leon"
counties["STL"]="St. Lucie"
counties["LEV"]="Levy"
counties["BRE"]="Brevard"
counties["LIB"]="Liberty"
counties["CIT"]="Citrus"
counties["MAD"]="Madison"
counties["FLA"]="Flagler"
counties["NAS"]="Nassau"
counties["HER"]="Hernando"
counties["OKA"]="Okaloosa"
counties["LAK"]="Lake"
counties["SAN"]="Santa Rosa"
counties["MRN"]="Marion"
counties["SUW"]="Suwannee"
counties["ORA"]="Orange"
counties["TAY"]="Taylor"
counties["OSC"]="Osceola"
counties["UNI"]="Union"
counties["PUT"]="Putnam"
counties["WAK"]="Wakulla"
counties["SEM"]="Seminole"
counties["WAL"]="Walton"
counties["STJ"]="St. Johns"
counties["WAS"]="Washington"
counties["SUM"]="Sumter"
counties["CHA"]="Charlotte"
counties["VOL"]="Volusia"
counties["CLL"]="Collier"


#
#   Note that this is not performant, and is assumed to not need to be so
#
def county_name(abbrev):
    return counties[abbrev]


#   Definitions for voter status fields
voter_status = dict()
voter_status['ACT']='Active'
voter_status['PRE']='Preregister Minors'
voter_status['INA']='Inactive'

def voter_status_name(abbrev):
    return voter_status[abbrev]


race_code = dict()
race_code['1']='American Indian or Alaskan Native'
race_code['2']='Asian Or Pacific Islander'
race_code['3']='Black, Not Hispanic'
race_code['4']='Hispanic'
race_code['5']='White, Not Hispanic'
race_code['6']='Other'
race_code['7']='Multi-racial'
race_code['9']='Unknown'


def race_code_to_name(abbrev):
    return race_code[abbrev]


def race_code_from_name(name):
    for c, n in race_code:
        if n == name:
            return c
    return None




party_code = dict()
party_code['AIP']='American’s Party of Florida'
party_code['CPF']='Constitution Party of Florida'
party_code['DEM']='Florida Democratic Party'
party_code['ECO']='Ecology Party of Florida'
party_code['GRE']='Green Party of Florida'
party_code['IDP']='Independence Party of Florida'
party_code['INT']='Independent Party of Florida'
party_code['LPF']='Libertarian Party of Florida'
party_code['NPA']='No Party Affiliation'
party_code['PSL']='Party for Socialism and Liberation - Florida'
party_code['REF']='Reform Party'
party_code['REP']='Republican Party of Florida'

def party_code_name(abbrev):
    return party_code[abbrev]


history_columns = []
history_columns.append('County Code')
history_columns.append('Voter ID')
history_columns.append('Election Date')
history_columns.append('Election Type')
history_columns.append('History Code')



history_codes = dict()
history_codes['F']='Provisional Ballot – Early Vote'
history_codes['Z']='Provisional Ballot – Vote at Poll'
history_codes['A']='Voted Absentee'
history_codes['B']='Absentee Ballot NOT Counted'
history_codes['E']='Voted Early'
history_codes['N']='Did Not Vote (not all counties use this code nor are required to report this data)'
history_codes['P']='Provisional Ballot Not Counted'
history_codes['Y']='Voted at Polls'

def history_codes_name(abbrev):
    return history_codes[abbrev]


election_types = dict()
election_types['PPP']='Presidential Primary'
election_types['PRI']='Primary'
election_types['RUN']='Run-off'
election_types['GEN']='General Election'
election_types['OTH']='Special/Local/Municipal/Other'

def election_types_name(abbrev):
    return election_types[abbrev]

