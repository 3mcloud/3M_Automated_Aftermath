import pandas as pd
import pyodbc
from pathlib import Path
import time
import pickle as pickle


#DATA_DIRECTORY = Path('./data')
pkl_data_fp = './pkl/data_HCG.pkl'
start = time.time()
with open(pkl_data_fp, 'rb') as f:
    data = pickle.load(f)
print('data load time {:.2f} seconds'.format(time.time() - start))


print(data.keys())
#Modify query by institute type
hd2018 = data['HD2018'].copy()
c2018c = data['C2018_C'].copy()

print(type(hd2018))

# URM : under-represented minority = American Indian or Alaska Native total + Black or African American total +
# Hispanic or Latino total + Native Hawaiian or Other Pacific Islander total
# URM does not include Asian total + Race/ethnicity unknown total + More than one ethnicity total
c2018c['URM'] = c2018c['CSAIANT'] + c2018c['CSBKAAT'] + c2018c['CSHISPT'] + c2018c['CSNHPIT']

c2018c_g = c2018c.groupby('UNITID', as_index=False).sum()   # sum over award levels - change to select BS only
c2018c_g = c2018c_g.merge(hd2018, how='left', on='UNITID')

#c2018c_g = c2018c.groupby('SECTOR', as_index=False)

c2018c_g['URM_PCT'] = c2018c_g['URM'] / c2018c_g['CSTOTLT']

top_10_urm = c2018c_g.sort_values(by='URM', ascending=False).head(10)[['INSTNM', 'CSTOTLT', 'URM']]
print(top_10_urm)

top_10_urm_pct = c2018c_g.sort_values(by='URM_PCT', ascending=False).head(10)[['INSTNM', 'CSTOTLT', 'URM', 'URM_PCT']]
print(top_10_urm_pct)