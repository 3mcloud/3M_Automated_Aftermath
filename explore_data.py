# %% setup
import numpy as np
import pandas as pd
import pyodbc
from pathlib import Path
import time
import pickle
import os
import matplotlib.pyplot as plt

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


# %% utils for reading data from access databases and save them as pkl files

print('no need to re-read access files if you have the pickle files')
# odbc = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]  # check if ms access ACE odbc is available
# assert bool(odbc), 'MS Access ACE odbc is not available'


def read_db(db_fp, table_name) -> pd.DataFrame:
    """
    reads table_name from access db_fp
    :param db_fp: file path to access file
    :param table_name: string
    :return: pandas dataframe
    """
    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' % db_fp
    conn = pyodbc.connect(odbc_conn_str)
    qry = f'SELECT * FROM {table_name}'
    df = pd.read_sql(qry, conn)
    conn.close()
    return df


def read_graduation_data(data_dir) -> dict:
    start = time.time()
    per_year = [i for i in data_dir.iterdir()]
    print(f'loading tables from {len(per_year)} access databases... will take a while.\nGo grab a coffee...')
    data_dict = {}

    for year_path in per_year:
        db_fp = [i for i in year_path.glob('*.accdb')][0]

        year_num = year_path.name[6:10]
        relevant_tables = [f'HD{year_num}', f'C{year_num}_A', f'C{year_num}_C']  # HD2019 institutions, C2019_A Conferred

        for table_name in relevant_tables:
            try:
                data_dict[table_name] = read_db(db_fp, table_name)
            except:
                print(table_name, 'did not exist for ', year_num, '!')  # some tables do not exist for older years.
    print('time spent: {:.2f} minutes'.format((time.time() - start)/60))
    return data_dict


def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


# data = read_graduation_data(DATA_DIRECTORY)  # reads from access - don't need to re-run this if you have pkl files
#
# save_obj(data, './pkl/data_2018-2019.pkl')
#
# t = time.time()
# data = load_obj('./pkl/data_HCG.pkl')
# print(time.time() - t, 'seconds')   # takes 6 seconds to load the data instead of 8.2 minutes
print()

# %% which universities have more "number of URM students receiving BS awards/degrees"


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


print(urm_students_large_inst(data, 2019, method='absolute'))

# %% which universities have more "number of awards/degrees" for urm students in math


def find_major_universities(data_dict, year, min_awards=5e4) -> pd.DataFrame:
    """
    finds the universities that awarded at least min_awards number of degrees or certificates (all levels)
    :param year : int
    :param min_awards: int or float - minimum number of degrees awarded
    :return: pd.DataFrame (or Series) containing UNITID of major universities
    """
    c20xxa = data_dict[f'C{year}_A'].copy()
    dx = c20xxa.copy()

    dx.CIPCODE = dx.CIPCODE.astype('float')
    dx = dx[dx.CIPCODE.isin(list(np.arange(0, 100)))]  # because of sum, do not re-count cip code sub-categories

    dx = dx[dx.MAJORNUM == 1]  # count only the first majors

    # find the unitid of large universities as defined by those that awarded at least min_awards BS degrees
    uni_g = dx.groupby(by='UNITID', as_index=False).sum()
    major_uni = uni_g[uni_g.CTOTALT > min_awards]['UNITID']

    return major_uni


def urm_degrees_large_inst(data_dict, year, university_specific, method='absolute', min_awards=5e4):
    """
    returns top 10 institutions that have highest "number of awards/degrees" for URM students in math
    returns top 10 institutions that have highest "number of awards/degrees" for URM students in math with cip breakdown
    :param data_dict: dict containing (key= table_name, value=table as pd.DataFrame)
    :param year: int
    :param method: str in ['absolute', 'percentage']
    :param min_awards: int - include only institutions that awarded at least min_awards number of degrees
    :return: pd.DataFrame, pd.DataFrame
    """

    assert year in np.arange(2011, 2020), 'This data is only available in years 2011-2019, inclusive!'

    hd20xx = data_dict[f'HD{year}'].copy()
    c20xxa = data_dict[f'C{year}_A'].copy()

    # major_uni = find_major_universities(c20xxa, min_awards=min_awards)
    major_uni = university_specific
    # print(major_uni.shape)

    dx = c20xxa[c20xxa.CIPCODE.isin(list(CIP_CODES_OF_INTEREST.keys()))].copy()  # only relevant cip codes
    dx['URM'] = dx['CAIANT'] + dx['CBKAAT'] + dx['CHISPT'] + dx['CNHPIT']  # calculate under represented minority
    dx = dx[dx.AWLEVEL == 5]  # only bachelor's degrees
    dx = dx[dx.MAJORNUM == 1]  # only the first major (counting second majors means counting one person twice) #Talk with Kyndra about preferences

    dx_sum = dx.groupby('UNITID', as_index=False).sum()  # total conferral for the selected cip codes
    dx_sum = dx_sum[dx_sum.UNITID.isin(list(major_uni))]  # filter to only large universities
    #dx_sum = dx_sum[dx_sum.CTOTALT > 10]  # filter to only universities that awarded at least 10 BS in CIPs

    dx_sum = dx_sum.merge(hd20xx, how='left', on='UNITID')
    dx_sum['URM_PCT'] = 100 * dx_sum['URM'] / dx_sum['CTOTALT']

    if method == 'absolute':
        top_10 = dx_sum.sort_values(by='URM', ascending=False).head(10)[['UNITID', 'INSTNM', 'CTOTALT', 'URM']]
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

    os.makedirs('results', exist_ok=True)
    top_10.to_json(Path(r'results/top_10_unis.json'))  # save to json file - TODO filepath as input argument
    dx_10.to_json(Path(r'results/top_10_unis_detail.json'))  # save to json file
    return top_10, dx_10


uni_list = find_major_universities(data, 2019, min_awards=4e4)
best_unis, best_unis_detail = urm_degrees_large_inst(data, 2019, uni_list, method='absolute', min_awards=4e4)
print(best_unis)
print()
print(best_unis_detail)

uni_list = best_unis.UNITID
best_unis, _ = urm_degrees_large_inst(data, 2018, uni_list, method='absolute', min_awards=4e4)
print(best_unis)
print(_)

# %% top regions or states with most "number of BS degrees awarded" to URM students in MATH
print()
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


# top_10_states_2019 = urm_degrees_top_states(data, 2019, key='region', method='absolute', top=10)
# print(top_10_states_2019)
print()
# %% plotting state histories
def plot_state_history(data_dict, key='state', method='percentage', specific_states=None):
    """
    doesn't really work generically yet - modified before the deadline to get a few plots
    """
    res = {}
    for year in np.r_[2011:2020]:
        res[year] = urm_degrees_top_states(data_dict, year, key, method, top=100)

    if method == 'percentage':
        v = 'URM_PCT'
    else:
        v = 'URM'

    if key == 'state':
        varname = 'STABBR'
    if key == 'region':
        varname = 'REGION'

    if specific_states is not None:
        state_list = specific_states
    else:
        state_list = res[2019][varname]

    d = {}

    sort_util = np.zeros(len(state_list))  # assuming 10 states - used to sort the legend
    for j, state in enumerate(state_list):
        d[state] = np.zeros((9, 2))
        for i, year in enumerate(np.r_[2011:2020]):
            x = res[year]
            d[state][i, 0] = year
            d[state][i, 1] = x[x[varname] == state][v]
            if year == 2019:
                sort_util[j] = d[state][i, 1]
        # plt.plot(d[state][:, 0], d[state][:, 1])
    print(sort_util)
    print(np.argsort(sort_util))
    specific_states_sort = [specific_states[i] for i in np.argsort(sort_util)[::-1]]

    if key == 'state':
        fig_size = [10, 4]
        xlim = [2010.5, 2022]
    if key == 'region':
        fig_size = [15, 4]
        xlim = [2010.5, 2025]
    plt.figure(figsize=fig_size)
    for state in specific_states_sort:
        plt.plot(d[state][:, 0], d[state][:, 1])
    plt.legend(list(specific_states_sort))
    if method == 'percentage':
        plt.ylim([0, 15])
        plt.ylabel("Percent of Degrees Awarded to URMs")
    else:
        plt.ylabel("Number of Degrees Awarded to URMs")
        plt.ylim([0, 150])

    plt.xlim(xlim)
    plt.xticks(ticks=np.r_[2011:2020], labels=np.r_[2011:2020])
    # plt.ylabel(v)
    plt.xlabel('Year')
    if key=='state':
        plt.title('History of Top 10 States or Territories in 2019 - PhD Awarded to URMs - All Math Majors')
    if key=='region':
        plt.title('History of Region - PhD Awarded to URMs - All Math Majors')
    plt.show()
    return d

# top_states = urm_degrees_top_states(data, 2019, key='state', method='absolute', top=10)

d = plot_state_history(data, key='state', method='percentage', specific_states=['WI', 'MI', 'MN', 'IL', 'IN', 'OH'])  # list or top_states.STABBR or top_states.REGION
# print(top_states)


# %% history of the top 10 universities from 2019


def history_best_unis_2019(data_dict, method='percentage', min_awards=5e4):
    res = {}

    uni_list = find_major_universities(data_dict, 2019, min_awards=4e4)
    best_unis, best_unis_detail = urm_degrees_large_inst(data_dict, 2019, uni_list, method=method, min_awards=min_awards)
    res[2019] = best_unis

    uni_list = best_unis.UNITID

    for year in np.r_[2011:2019]:
        # print(year)
        res[year], _ = urm_degrees_large_inst(data_dict, year, uni_list, method=method, min_awards=min_awards)

    os.makedirs('results', exist_ok=True)
    with open('results/hist_of_top_10_2019.pkl', 'wb') as f:
        pickle.dump(res, f)
    return res


result = history_best_unis_2019(data, method='absolute')
print(result[2019])


def plot_history(res_hist, method='percentage'):
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


d = plot_history(result, method='absolute')


