import numpy as np

A = [1,2,3]
passed = 'A'

print(eval(passed))

year_N = 2010

assert year_N in np.arange(2011, 2020), 'This data is only available in years 2011-2019, inclusive!'