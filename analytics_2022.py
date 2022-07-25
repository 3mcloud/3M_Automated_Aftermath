import argparse
import os
import numpy as np
import sys
import pandas as pd
import pickle
import time
import pyodbc
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
from typing import Union
from fastapi import FastAPI



"""
Notes:
URM : under-represented minority = American Indian or Alaska Native total + Black or African American total +
            Hispanic or Latino total + Native Hawaiian or Other Pacific Islander total
URM does not include Asian total or Race/ethnicity unknown total

degree_level_codes: { 1: less than 1 academic year, 2:  at least 1 but less than 4 academic years,
    3: Associate's degree, 5: Bachelor's degree, 7: Master's degree, 9: Doctor's degree,
    10: Postbaccalaureate or Post-master's certificate }
"""

CIP_CODES_OF_INTEREST = {
    '13.1311': 'Mathematics Teacher Education',
    '27.0101': 'Mathematics, General',
    '27.0199': 'Mathematics, Other',
    '27.0301': 'Applied Mathematics, General',
    '27.0303': 'Computational Mathematics',
    '27.0304': 'Computational And Applied Mathematics',
    '27.0305': 'Financial Mathematics',
    '27.0306': 'Mathematical Biology',
    '27.0399': 'Applied Mathematics, Other',
    '27.0502': 'Mathematical Statistics And Probability',
    '27.0503': 'Mathematics And Statistics',
    '27.9999': 'Mathematics And Statistics, Other',
    '30.0801': 'Mathematics And Computer Science',
    '40.0810': 'Theoretical And Mathematical Physics'
}

CIP_ED = {'13.1311': 'Mathematics Teacher Education'}
CIP_GEN = {'27.0101': 'Mathematics, General'}
CIP_OTHER = {'27.0199': 'Mathematics, Other'}
CIP_APP_MATH = {'27.0301': 'Applied Mathematics, General',
    '27.0303': 'Computational Mathematics',
    '27.0304': 'Computational And Applied Mathematics',
    '27.0305': 'Financial Mathematics',
    '27.0306': 'Mathematical Biology',
    '27.0399': 'Applied Mathematics, Other'}
CIP_MATH_STAT = {'27.0502': 'Mathematical Statistics And Probability',
    '27.0503': 'Mathematics And Statistics',
    '27.9999': 'Mathematics And Statistics, Other'}
CIP_MATH_CS = {'30.0801': 'Mathematics And Computer Science',}
CIP_MATH_PHYS = {'40.0810': 'Theoretical And Mathematical Physics'}

# Bureau of Economic Analysis (BEA) regions CODES
OBEREG = {
    0: 'U.S. Service schools',
    1: 'New England (CT, ME, MA, NH, RI, VT)',
    2: 'Mid East (DE, DC, MD, NJ, NY, PA)',
    3: 'Great Lakes  (IL, IN, MI, OH, WI)',
    4: 'Plains (IA, KS, MN, MO, NE, ND, SD)',
    5: 'Southeast (AL, AR, FL, GA, KY, LA, MS, NC, SC, TN, VA, WV)',
    6: 'Southwest (AZ, NM, OK, TX)',
    7: 'Rocky Mountains (CO, ID, MT, UT, WY)',
    8: 'Far West (AK, CA, HI, NV, OR, WA)',
    9: 'Other U.S. jurisdictions (AS, FM, GU, MH, MP, PR, PW, VI)'
}

def parse_args(args: List[str]) -> argparse.Namespace:
    # Argument Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--gender', default='all', type=str, help='What genders to include', choices=['all', 'male', 'female'])
    parser.add_argument('--degree', default='all', nargs='+', type=str, help='Degrees to include')
    parser.add_argument('--start_year', default='2019', type=int, help="First year in analysis range")
    parser.add_argument('--end_year', default='2019', type=int, help="Last year in analysis range")
    parser.add_argument('--min_awards_granted', default=0, type=int, help='Minimum number of degrees granted by institution per year')
    parser.add_argument('--citizenship', default='US', type=str, help="Citizenships to consider", choices=['US', 'non-resident', 'all']) 
    parser.add_argument('--degree_cip', default='all', type=str, help='Concentration-type of degree granted')
    parser.add_argument('--university_type', default='all', type=str, help='University type', choices = ['all','public','private not-for-profit', 'private for-profit'])
    parser.add_argument('--uni_degree_type', default='any', type=str, help='Highest degree granted by university', choices=['PhD', 'MS', 'BS', 'A', 'any'])
    parser.add_argument('--geo_region_max', default='all', type=str, help='Largest geographic region of the US', choices=['all', 'states', 'contiguous_48'])
    parser.add_argument('--bea_region', default='all', nargs='+', 
                        type=str, help='BEA-designated regions of the 50 states ',
                        choices=['all', 'New England', 'Mid East', 'Great Lakes', 'Plains',
                        'Southeast', 'Southwest','Rocky Mountains', 'Far West', 'Other U.S. jurisdictions'])
    parser.add_argument('--state', default='', type=str, nargs='+', help='Individual state(s) to investigate')
    
    return parser.parse_args(args[1:])

def specify_locations(geo_region, obereg, states = None):
    '''Function to limit analyzed data to only geographic regions of interest.  Returns a list of states to be included.'''

    incl_states = []
    if states is not None:




if __name__ == '__main__':

    # This code will be irrelevant when connected to the frontend, but is in place now to test the analysis functions.

    # Parse command line arguments
    ARGS = parse_args(sys.argv)

    #For now, hard-coding selections

    gender = ARGS.gender
    degree = ARGS.degree
    year_0 = ARGS.start_year
    year_N = ARGS.end_year
    citizen = ARGS.citizenship
    cip = ARGS.degree_cip
    min_awards = ARGS.min_awards_granted
    uni_type = ARGS.university_type
    hdeg = ARGS.uni_degree_type
    geo_region = ARGS.geo_region_max
    obereg = ARGS.bea_region
    states = ARGS.state

    print('Degrees included: ', degree)

    if cip == 'all':
        cip = [CIP_ED, CIP_GEN, CIP_OTHER, CIP_APP_MATH, CIP_MATH_STAT, CIP_MATH_CS, CIP_MATH_PHYS]

    #Load local data dir.  This will need to be updated as discussed with Lily.
    DATA_DIRECTORY = Path('./data')
    pkl_data_fp = './pkl/data_HCG.pkl'
    start = time.time()
    with open(pkl_data_fp, 'rb') as f:
        data = pickle.load(f)
    print('data load time {:.2f} seconds'.format(time.time() - start))

    # pandas display options
    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', None)
    pd.set_option('display.width', 320)

    #geography = None
    geography = specify_locations(geo_region, obereg, states)

    best_unis, best_unis_detail = urm_degrees(data, year_N, citizen, gender, degree, cip, geography, hdeg, uni_type, min_awards, method='absolute')

    #print(best_unis)
    print(best_unis_detail)
    #(data_dict, year, citizenship, gender, degree, cip, geography, hdeg, uni_type, min_awards, method='absolute', specific_universities=None):