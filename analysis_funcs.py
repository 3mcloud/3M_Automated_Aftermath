import argparse
import plotly
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

#Line plot.  Probably not using at all as there is a plotly specific to react
def visualize_line_time_series(data_frame, y_values, y_label, time_label):
    '''line plot visualization'''
    data_tuples = list(zip(data_frame[time_label],y_values))
    frame = pd.DataFrame(data_tuples, columns=['Date',y_label])
    import plotly.express as px
    fig = px.line(frame, x="Date", y=y_label)
    fig.show()


def find_major_universities(data_dict, year, min_awards=5e4) -> pd.DataFrame:
    """
    finds the universities that awarded at least min_awards number of degrees or certificates (all levels)
    :param data_dict: dict containing (key= table_name, value=table as pd.DataFrame)
    :param year : int
    :param min_awards: int or float - minimum number of degrees awarded
    :return: pandas.core.series.Series containing UNITID of major universities
    """
    dx = data_dict[f'C{year}_A'].copy()
    #Nader, your code splits this line into two.  Was there any reason for this?

    dx.CIPCODE = dx.CIPCODE.astype('float')
    dx = dx[dx.CIPCODE.isin(list(np.arange(0, 100)))]  # because of sum, do not re-count cip code sub-categories

    dx = dx[dx.MAJORNUM == 1]  # count only the first majors

    # find the unitid of large universities as defined by those that awarded at least min_awards BS degrees
    uni_g = dx.groupby(by='UNITID', as_index=False).sum()
    major_uni = uni_g[uni_g.CTOTALT > min_awards]['UNITID']

    return major_uni


def urm_students_large_inst(data_dict, year, method='absolute', min_students=5000):
    """
    returns top 10 universities that have most urm students with bachelor's degrees
    CONDITIONED ON the university having at least min_students bachelor's degrees
    :param data_dict: dict containing (key= table_name, value=table as pd.DataFrame)
    :param year: int
    :param method: str in ['absolute', 'percentage']
    :param min_students: int
    :return: pd.DataFrame
    """

    ##TODO Nader, is this function only exploratory and not actually used for any of the visualizations you showed?
    #Do we need to functionalize it?

    assert year in np.arange(2012, 2020), 'This data is only available in years 2012-2019, inclusive!'

    hd20xx = data_dict[f'HD{year}'].copy()
    c20xxc = data_dict[f'C{year}_C'].copy()
    c20xxc['URM'] = c20xxc['CSAIANT'] + c20xxc['CSBKAAT'] + c20xxc['CSHISPT'] + c20xxc['CSNHPIT']

    # c2018c_g = c2018c.groupby('UNITID', as_index=False).sum()   # sum over award levels - change to select BS only
    c20xxc_g = c20xxc[c20xxc.AWLEVELC == 5]  # bachelor's degree only
    c20xxc_g = c20xxc_g[c20xxc_g.CSTOTLT >= min_students]  # at least num_students bachelor's degree only

    c20xxc_g = c20xxc_g.merge(hd20xx, how='left', on='UNITID')

    c20xxc_g['URM_PCT'] = 100 * c20xxc_g['URM'] / c20xxc_g['CSTOTLT']
    if method == 'absolute':
        return c20xxc_g.sort_values(by='URM', ascending=False).head(10)[['INSTNM', 'CSTOTLT', 'URM']].set_axis(np.arange(0, 10), axis=0)
    elif method == 'percentage':
        return c20xxc_g.sort_values(by='URM_PCT', ascending=False).head(10)[['INSTNM', 'CSTOTLT', 'URM', 'URM_PCT']].set_axis(np.arange(0, 10), axis=0)

    ## Nader, this seems to be recursive?  Should this print statement be one tab back?  
    # Also, it seems that we're not actually doing anything with urm_students_large_inst
    print(urm_students_large_inst(data, 2019, method='absolute'))


def top_10_num_urm_students(data_dict, year, degree, method='absolute'):
    """
    returns top 10 universities that have most urm students with degrees of interest
    :param data_dict: dict containing (key= table_name, value=table as pd.DataFrame)
    :param year: int
    :param degree: list
    :param method: str in ['absolute', 'percentage']
    :param min_students: int
    :return: pd.DataFrame
    """

    assert year in np.arange(2012, 2020), 'This data is only available in years 2012-2019, inclusive!'

    hd20xx = data_dict[f'HD{year}'].copy()
    c20xxc = data_dict[f'C{year}_C'].copy()
    c20xxc['URM'] = c20xxc['CSAIANT'] + c20xxc['CSBKAAT'] + c20xxc['CSHISPT'] + c20xxc['CSNHPIT']

    AWLEVELS = []
    if 'BS' in degree:
        AWLEVELS.append(5)
    if 'A' in degree:
        AWLEVELS.append(3)
    if 'MS' in degree:
        AWLEVELS.append(7)
    if 'PhD' in degree:
        AWLEVELS.extend([17, 18, 19])

    #print(AWLEVELS)

    c20xxc_g = c20xxc[c20xxc.AWLEVELC == any(AWLEVELS)]

    #c20xxc_g = c20xxc_g[c20xxc_g.CSTOTLT >= min_students]  # at least num_students bachelor's degree only

    c20xxc_g = c20xxc_g.merge(hd20xx, how='left', on='UNITID')

    c20xxc_g['URM_PCT'] = 100 * c20xxc_g['URM'] / c20xxc_g['CSTOTLT']
    if method == 'absolute':
        res = c20xxc_g.sort_values(by='URM', ascending=False).head(10)[['INSTNM', 'CSTOTLT', 'URM']].set_axis(np.arange(0, 10), axis=0)

    elif method == 'percentage':
        res = c20xxc_g.sort_values(by='URM_PCT', ascending=False).head(10)[['INSTNM', 'CSTOTLT', 'URM', 'URM_PCT']].set_axis(np.arange(0, 10), axis=0)

    else:
        res = None  # cute exception handling :D

    # save results to disk in json for ethan
    os.makedirs('results', exist_ok=True)
    res.to_json(Path(r'results/top_10_unis_student.json'))  # save to json file - filename convention needed

    return res


def urm_degrees(data_dict, year, citizenship, gender, degree, cip, geography, hdeg, uni_type, min_awards, method='absolute', specific_universities=None):
    """
    returns top 10 institutions that have highest "number of awards/degrees" for URM students in math
    returns top 10 institutions that have highest "number of awards/degrees" for URM students in math with cip breakdown
    :param data_dict: dict containing (key= table_name, value=table as pd.DataFrame)
    :param year: int
    :param citizenship:
    :param gender:
    :param cip:
    :param geography:
    :param hdeg:
    :param method: str in ['absolute', 'percentage']
    :param specific_universities : pd.Series list of universities to limit search - default None for all inclusive search
    :return: pd.DataFrame, pd.DataFrame
    """

    assert year in np.arange(2011, 2020), 'This data is only available in years 2011-2019, inclusive!'

    hd20xx = data_dict[f'HD{year}'].copy()
    c20xxa = data_dict[f'C{year}_A'].copy()

    if specific_universities is not None:
        major_uni = specific_universities
    else:
        major_uni = find_major_universities(data_dict, year, min_awards)  # include all universities

    #print('hdkeys', hd20xx.keys())
    #print('c20keys', c20xxa.keys())

    cip_list = []
    #identify all selected cip codes
    #print(cip)
    for major_group in cip:
        #print('major_group', major_group.keys())
        cip_list.extend(x for x in major_group.keys())

    #Filter by CIP codes selected
    dx = c20xxa[c20xxa.CIPCODE.isin(cip_list)].copy()  # only relevant cip codes

    # calculate under-represented minority for different groupings
    dx['URM'] = dx['CAIANT'] + dx['CBKAAT'] + dx['CHISPT'] + dx['CNHPIT'] 
    dx['URM_female'] = dx['CAIANW'] + dx['CBKAAW'] + dx['CHISPW'] + dx['CNHPIW'] 
    dx['URM_male'] = dx['CAIANM'] + dx['CBKAAM'] + dx['CHISPM'] + dx['CNHPIM'] 
    dx['URM_female_nonresident'] = dx['CNRALW']
    dx['URM_male_nonresident'] = dx['CNRALM']
    dx['URM_nonresident'] = dx['CNRALW'] + dx['CNRALM']
    dx['URM_female_US'] = dx['URM_female'] - dx['URM_female_nonresident']
    dx['URM_male_US'] = dx['URM_male'] - dx['URM_male_nonresident']
    dx['URM_US'] = dx['URM'] - dx['URM_nonresident']


    #filter by selected degrees
    AWLEVELS = []
    if 'BS' in degree:
        AWLEVELS.append(5)
    if 'A' in degree:
        AWLEVELS.append(3)
    if 'MS' in degree:
        AWLEVELS.append(7)
    if 'PhD' in degree:
        AWLEVELS.extend([17, 18, 19])

    #Filter by selected degrees
    dx = dx[dx.AWLEVEL == any(AWLEVELS)]
    #dx = dx[dx.AWLEVEL == 5]  # only bachelor's degrees
    
    dx = dx[dx.MAJORNUM == 1]  # only the first major (counting second majors means counting one person twice) #Talk with Kyndra about preferences

    #Filter by gender and citizenship if selected
    if gender == 'all' and citizenship == 'all':
        subgroup_selector = 'URM'
    elif gender == 'male' and citizenship == 'all':
        subgroup_selector = 'URM_male'
    elif gender == 'female' and citizenship == 'all':
        subgroup_selector = 'URM_female'
    elif gender == 'all' and 'citizenship' == 'US':
        subgroup_selector = 'URM_US'
    elif gender == 'male' and citizenship == 'US':
        subgroup_selector = 'URM_male_US'
    elif gender == 'female' and citizenship == 'US':
        subgroup_selector = 'URM_female_US'
    elif gender == 'all' and 'citizenship' == 'non-resident':
        subgroup_selector = 'URM_nonresident'
    elif gender == 'male' and citizenship == 'non-resident':
        subgroup_selector = 'URM_male_nonresident'
    elif gender == 'female' and citizenship == 'non-resident':
        subgroup_selector = 'URM_female_nonresident'
    else:
        print('Submitted gender specification or citizenship specification not in the data')

    #Filter by highest degree conferred by university
    if hdeg == 'PhD':
        hd = hd20xx[hd20xx.HDEGOFR1==11]+ hd20xx[hd20xx.HDEGOFR1==12] + hd20xx[hd20xx.HDEGOFR1==13] + hd20xx[hd20xx.HDEGOFR1==14]
    elif hdeg == 'MS':
        hd = hd20xx[hd20xx.HDEGOFR1==20]
    elif hdeg == 'BS':
        hd = hd20xx[hd20xx.HDEGOFR1==30]
    elif hdeg == 'A':
        hd = hd20xx[hd20xx.HDEGOFR1==40]
    elif hdeg == 'any':
        hd = hd20xx

    #Filter by uni_type
    sector = []
    for utype in uni_type:
        if utype == 'public':
            sector.extend([1,4,7])
        elif utype == 'private not-for-profit':
            sector.extend([2, 5, 8])
        elif utype == 'private for-profit':
            sector.extend([3,6,9])

    hd = hd[hd.SECTOR == any(sector)]

    #Filter by geography?


    dx_sum = dx.groupby('UNITID', as_index=False).sum()  # total conferral for the selected cip codes
    dx_sum = dx_sum[dx_sum.UNITID.isin(list(major_uni))]  # filter to only large universities
    #dx_sum = dx_sum[dx_sum.CTOTALT > 10]  # filter to only universities that awarded at least 10 BS in CIPs

    dx_sum = dx_sum.merge(hd, how='left', on='UNITID')
    dx_sum['URM_PCT'] = 100 * dx_sum['URM'] / dx_sum['CTOTALT']

    if method == 'absolute':
        top_10 = dx_sum.sort_values(by='URM', ascending=False).head(10)[['UNITID', 'INSTNM', 'CTOTALT', subgroup_selector]]
        top_10 = top_10.set_axis(np.arange(0, top_10.shape[0]), axis=0)
        dx_10 = dx[dx.UNITID.isin(top_10.UNITID)]
        dx_10 = dx_10[dx_10.URM != 0]
        dx_10 = dx_10.merge(hd20xx, how='left', on='UNITID')
        # print(dx_10.columns)
        dx_10 = dx_10[['UNITID', 'CIPCODE', 'INSTNM', 'CTOTALT', 'URM']].sort_values(by=['UNITID', 'CIPCODE'])
        dx_10.set_axis(np.arange(0, dx_10.shape[0]), axis=0, inplace=True)

    elif method == 'percentage':
        top_10 = dx_sum.sort_values(by='URM_PCT', ascending=False).head(10)[['UNITID', 'INSTNM', 'CTOTALT', 'URM', 'URM_PCT']]
        top_10 = top_10.set_axis(np.arange(0, top_10.shape[0]), axis=0)
        dx_10 = dx[dx.UNITID.isin(top_10.UNITID)].copy()
        dx_10 = dx_10[dx_10.URM != 0]
        dx_10['URM_PCT'] = 100 * dx_10['URM'] / dx_10['CTOTALT']
        dx_10 = dx_10.merge(hd20xx, how='left', on='UNITID')[['UNITID', 'CIPCODE', 'INSTNM', 'CTOTALT', 'URM', 'URM_PCT']].sort_values(by=['UNITID', 'CIPCODE'])
        dx_10.set_axis(np.arange(0, dx_10.shape[0]), axis=0, inplace=True)

    else:  # cute management :D
        top_10, dx_10 = None, None

    # save results to disk in json for ethan
    os.makedirs('results', exist_ok=True)
    top_10.to_json(Path(r'results/top_10_unis_degree.json'))  # save to json file -  filename convention needed
    dx_10.to_json(Path(r'results/top_10_unis_degree_detail.json'))  # save to json file
    return top_10, dx_10


# TODO this function was migrated from explore_data.py on 20210805
def urm_degrees_top_states(data_dict, year, key='state', method='absolute', top=100):
    """
    returns top states/regions with most BS in MATH degrees awarded to URM
    :param data_dict: dict containing (key= table_name, value=table as pd.DataFrame)
    :param year: int (range 2011-2019)
    :param key: str in ['state', 'region']
    :param method: str in ['percentage', 'absolute']
    :param top: int (number of top states to return)
    :return: pd.DataFrame
    """
    assert year in np.arange(2011, 2020), 'This data is only available in years 2011-2019, inclusive!'
    hd20xx = data_dict[f'HD{year}'].copy()
    c20xxa = data_dict[f'C{year}_A'].copy()

    dx = c20xxa[c20xxa.CIPCODE.isin(list(CIP_CODES_OF_INTEREST.keys()))].copy()  # only relevant MATH cip codes
    dx['URM'] = dx['CAIANT'] + dx['CBKAAT'] + dx['CHISPT'] + dx['CNHPIT']  # calculate under represented minority
    dx = dx[dx.AWLEVEL == 5]  # only bachelor's degrees
    dx = dx[dx.MAJORNUM == 1]  # only the first major (counting second majors means counting one person twice)

    dx = dx.merge(hd20xx, how='left', on='UNITID')  # merge with university information

    if key == 'state':
        var_name = 'STABBR'
    elif key == 'region':
        var_name = 'OBEREG'
    else:
        ex = ValueError()
        ex.strerror = "key must be either 'state' or 'region'"
        raise ex  # :D

    dx = dx.groupby(var_name, as_index=False)[['CTOTALT', 'URM']].sum()

    if method == 'absolute':
        res = dx.sort_values(by='URM', ascending=False).head(top)

    if method == 'percentage':
        dx['URM_PCT'] = 100 * dx['URM'] / dx['CTOTALT']
        res = dx.sort_values(by='URM_PCT', ascending=False).head(top)

    if key == 'region':  # provide region names
        dtype_region = pd.CategoricalDtype(list(OBEREG.values()), ordered=True)
        res['REGION'] = pd.Categorical.from_codes(codes=res['OBEREG'], dtype=dtype_region)

    res = res.set_axis(np.arange(0, res.shape[0]), axis=0)

    os.makedirs('results', exist_ok=True)
    res.to_json(Path(r'results/top_10_states_or_regions.json'))  # save to json

    return res


# testing urm_degrees_top_states
# top_10_states_2019 = urm_degrees_top_states(data, 2019, key='region', method='percentage', top=10)
# print(top_10_states_2019)


def history_best_unis_2019(data_dict, method='percentage', min_awards=5e4):
    """
    find top 10 unis of 2019 - return their performance in 2019 and previous years
    the results can be manipulated to plot a timeline comparative performance history
    :param data_dict: dict containing (key= table_name, value=table as pd.DataFrame)
    :param method: str in ['absolute', 'percentage']
    :param min_awards: int to limit to only institutions that awarded at least min_awards degrees
    :return: dict of {key: year (int) -> value: top_10_universities (pd.DataFrame)}
    """
    res = {}

    uni_list = find_major_universities(data_dict, 2019, min_awards=min_awards)
    # TODO at the time of coding , 'degree, gender, geography' were not used in 'urm_degrees' - to be revised later
    top_10_2019, _ = urm_degrees(data_dict, 2019, citizenship='all', gender='all', degree='BS', cip='all', geography=0, hdeg='any', uni_type='all', min_awards = 500, method=method, specific_universities=uni_list)

    res[2019] = top_10_2019

    uni_list = top_10_2019.UNITID

    for year in np.r_[2011:2019]:
        res[year], _ = urm_degrees(data_dict, year, citizenship='all', gender='all', degree='BS', cip='all', geography=0, hdeg='any', uni_type='all', min_awards = 500, method=method, specific_universities=uni_list)

    os.makedirs('results', exist_ok=True)
    with open('results/hist_of_top_10_2019.pkl', 'wb') as f:
        pickle.dump(res, f)
    return res


# test history_best_unis_2019 quickly - works as of 06/22 - 6:33pm :D - Nader
# pkl_data_fp = './pkl/data_HCG.pkl'
# with open(pkl_data_fp, 'rb') as f:
#     data = pickle.load(f)
# result = history_best_unis_2019(data, method='percentage')


# TODO this function was migrated from explore_data.py on 20210805
def plot_history(result, method='percentage'):
    """
    result = history_best_unis_2019(data, method='percentage')
    """
    if method == 'percentage':
        v = 'URM_PCT'
    else:
        v = 'URM'
    d = {}
    plt.figure(figsize=[10, 4])
    for inst in result[2019].UNITID:
        d[inst] = np.zeros((9, 2))
        for i, year in enumerate(np.r_[2011:2020]):
            d[inst][i, 0] = year
            x = result[year]
            try:  # in case that university is not in the previous data
                d[inst][i, 1] = x[x.UNITID == inst][v]
            except:
                pass
        plt.plot(d[inst][:, 0], d[inst][:, 1])
    plt.legend(list(result[2019].INSTNM))

    plt.xlim([2010.5, 2026])
    plt.xticks(ticks=np.r_[2011:2020], labels=np.r_[2011:2020])
    if method == 'percentage':
        plt.ylabel("Percent of Degrees Awarded to URMs")
        plt.ylim([0, 100])
    else:
        plt.ylabel("Number of Degrees Awarded to URMs")
        plt.ylim([0, 100])


    plt.xlabel('Year')
    plt.title('History of Top 10 Universities in 2019 - Bachelors Awarded to URMs - All Math Majors')
    plt.show()
    return d


# d = plot_history(result, method='absolute')


if __name__ == '__main__':

    #leave for later in case we're not needing parsing
    # parse command line arguments
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

    geography = None
    #geography = specify_locations(geo_region, obereg, states)

    best_unis, best_unis_detail = urm_degrees(data, year_N, citizen, gender, degree, cip, geography, hdeg, uni_type, min_awards, method='absolute')

    #print(best_unis)
    print(best_unis_detail)
    #(data_dict, year, citizenship, gender, degree, cip, geography, hdeg, uni_type, min_awards, method='absolute', specific_universities=None):