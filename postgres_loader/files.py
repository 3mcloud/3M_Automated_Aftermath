# list of Access files, and parameters of interest
# disable/enable entries appropriately for the files you have present
# file names MUST match, and the files must contain the tables specified!

# table names must be specified as bytes, as this is what MBDTools expects when specifying columns

# IPEDS C only has the C20XX_C table 2012 and later, so other years are being left out

files = [
    # {"file_name": "IPEDS200405.accdb", "year": 2004,
    #     "tables_of_interest": [b'C2004_A', b'HD2004']},
    # {"file_name": "IPEDS200506.accdb", "year": 2005,
    #     "tables_of_interest": [b'C2005_A', b'HD2005']},
    # {"file_name": "IPEDS200607.accdb", "year": 2006,
    #     "tables_of_interest": [b'C2006_A', b'HD2006']},
    # {"file_name": "IPEDS200708.accdb", "year": 2007,
    #     "tables_of_interest": [b'C2007_A', b'HD2007']},
    # {"file_name": "IPEDS200809.accdb", "year": 2008,
    #     "tables_of_interest": [b'C2008_A', b'HD2008']},
    # {"file_name": "IPEDS200910.accdb", "year": 2009,
    #     "tables_of_interest": [b'C2009_A', b'HD2009']},
    # {"file_name": "IPEDS201011.accdb", "year": 2010,
    #     "tables_of_interest": [b'C2010_A', b'HD2010']},
    # {"file_name": "IPEDS201112.accdb", "year": 2011,
    #  "tables_of_interest": [b'C2011_A', b'HD2011']},
    {"file_name": "IPEDS201213.accdb", "year": 2012,
        "tables_of_interest": [b'C2012_A', b'C2012_B', b'C2012_C', b'HD2012']},
    {"file_name": "IPEDS201314.accdb", "year": 2013,
        "tables_of_interest": [b'C2013_A', b'C2013_B', b'C2013_C', b'HD2013']},
    {"file_name": "IPEDS201415.accdb", "year": 2014,
        "tables_of_interest": [b'C2014_A', b'C2014_B', b'C2014_C', b'HD2014']},
    {"file_name": "IPEDS201516.accdb", "year": 2015,
        "tables_of_interest": [b'C2015_A', b'C2015_B', b'C2015_C', b'HD2015']},
    {"file_name": "IPEDS201617.accdb", "year": 2016,
        "tables_of_interest": [b'C2016_A', b'C2016_B', b'C2016_C', b'HD2016']},
    {"file_name": "IPEDS201718.accdb", "year": 2017,
        "tables_of_interest": [b'C2017_A', b'C2017_B', b'C2017_C', b'HD2017']},
    {"file_name": "IPEDS201819.accdb", "year": 2018,
        "tables_of_interest": [b'C2018_A', b'C2018_B', b'C2018_C', b'HD2018']},
    {"file_name": "IPEDS201920.accdb", "year": 2019,
        "tables_of_interest": [b'C2019_A', b'C2019_B', b'C2019_C', b'HD2019']}
]
