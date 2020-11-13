
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[71]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[51]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[145]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    import pandas as pd
    import numpy as np
    import csv
    
    u = open ('university_towns.txt', 'r')
    towns = []
    states = []
    a = 'Albama'
    for line in u:
        if '[edit]' in line:
            b = line.find('[')
            a = line[:b]
        else:
            states.append(a)
            if line.find('  (') == -1:
                x = line.find(' (')
                y = line[:x]
            else:
                x = line.find('  (')
                y = line[:x]
            towns.append(y)
    
    s = {"State": states, "RegionName" : towns}
    df = pd.DataFrame(s)
    df.set_index("State", inplace = True)
    df = df.reset_index()
    
    
    return df
       

get_list_of_university_towns()



# In[78]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    import numpy as np
    
    s = pd.read_excel('gdplev.xls', skiprows = 220, parse_cols = 'E, G')
    s.columns = ['Quarter', 'GDP']
    for x in range(3, len(s)):
        if s.loc[x, 'GDP'] < s.loc[x-1, 'GDP'] and s.loc[x-1, 'GDP'] < s.loc[x-2, 'GDP']:
            return s.loc[x -1, 'Quarter']
        
    

get_recession_start()
    


# In[121]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    import numpy as np
    
    s = pd.read_excel('gdplev.xls', skiprows = 220, parse_cols = 'E, G')
    s.columns = ['Quarter', 'GDP']
    a = 0
    for x in range(3, len(s)):
        if s.loc[x, 'GDP'] < s.loc[x-1, 'GDP'] and s.loc[x-1, 'GDP'] < s.loc[x-2, 'GDP']:
            a = x-1
            break
    t = 0
    for x in range(a, len(s)-3):
        if s.loc[x, 'GDP'] < s.loc[x+1, 'GDP'] and s.loc[x+1, 'GDP'] < s.loc[x+2, 'GDP']:
            t = x + 2
            break 
    return s.loc[t, 'Quarter']
        
get_recession_end()


# In[120]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    import pandas as pd
    import numpy as np
    
    s = pd.read_excel('gdplev.xls', skiprows = 220, parse_cols = 'E, G')
    s.columns = ['Quarter', 'GDP']
    a = 0
    for x in range(3, len(s)):
        if s.loc[x, 'GDP'] < s.loc[x-1, 'GDP'] and s.loc[x-1, 'GDP'] < s.loc[x-2, 'GDP']:
            a = x-1
            break
    t = 0
    for x in range(a, len(s)-3):
        if s.loc[x, 'GDP'] < s.loc[x+1, 'GDP'] and s.loc[x+1, 'GDP'] < s.loc[x+2, 'GDP']:
            t = x + 2
            break
    
    minimum = s.loc[a, 'GDP']
    for x in range(a+1, t):
        minimum = min(minimum, s.loc[x, 'GDP'])
    s = s.set_index("GDP")
    return s.loc[minimum, 'Quarter']
        
    
get_recession_bottom()


# In[124]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''

    
    import pandas as pd
    
    df = pd.read_csv("City_Zhvi_AllHomes.csv")
    del df["RegionID"]
    del df["Metro"]
    del df["CountyName"]
    del df["SizeRank"]
    df['State'] = df['State'].replace(states)
    df = df.set_index(['State', 'RegionName'])
    y = []
    x = df.columns[:]
    for i in x:
        t = i[0:4]
        if int(i[0:4]) < 2000 or int(i[0:4]) >= 2017 :
            del df[i]
        else:
            if i[-2:] == '02' or i[-2:] == '01' or i[-2:] == '03':
                t +='q1'
            elif i[-2:] == '04' or i[-2:] == '05' or i[-2:] == '06':
                t +='q2'
            elif i[-2:] == '07' or i[-2:] == '08' or i[-2:] == '09':
                t +='q3'
            elif i[-2:] == '10' or i[-2:] == '11' or i[-2:] == '12':
                t +='q4'
            if t not in y: y.append(t)
        
    z = []
    for j in y:
        q = j[-1:]
        year = j[0:4]
        a = 0
        if q == '1':
            a = df[[year+"-01",year+"-02",year+"-03"]].mean(axis=1)
        elif q == '2':
            a = df[[year+"-04",year+"-05",year+"-06"]].mean(axis=1)
        elif q == '3':
            if year == '2016':
                a = df[[year+"-07",year+"-08"]].mean(axis=1)
            else: 
                a = df[[year+"-07",year+"-08",year+"-09"]].mean(axis=1)                
        elif q == '4':
            a = df[[year+"-10",year+"-11",year+"-12"]].mean(axis=1)
        df[j] = a
    
    for x in df.columns[:]:
        if "-" in x:
            del df[x]
        
    
    return df

convert_housing_data_to_quarters()


# In[147]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    uni = get_list_of_university_towns().copy()
    df = convert_housing_data_to_quarters().copy()
    uni['towns'] = True

    
    final = pd.merge(df, uni, how="outer", right_on=['State', 'RegionName'], left_index = True)
    final['towns'] = final['towns'].replace({np.NaN: False})
    
    
    rs = get_recession_start()
    rb = get_recession_bottom()
    yrs = int(rs[0:4])
    qrs = int(rs[-1:])
    yrb = int(rb[0:4])
    qrb = int(rb[-1:])
    
    quarter = []
    for x in range(yrs, yrb+1):
        for y in range(1, 5):
            if not (x == yrs and y < qrs) or  not (x == yrb and y > qrb):
                quarter.append(str(x) + 'q' + str(y))
    final = final[['State', 'RegionName', 'towns'] + quarter]
    final['ratio'] = final['2008q3']- final['2009q2']
    
    town_ratio = final[final['towns'] == True]['ratio']
    non_town_ratio = final[final['towns'] == False]['ratio']
    st, p_value = ttest_ind(town_ratio, non_town_ratio, nan_policy='omit',)
    diff = False
    if p_value < 0.01:
        diff = True
    
    better = "university town"
    if town_ratio.mean() > non_town_ratio.mean():
        better = "non-university town"

    return (diff, p_value, better)
run_ttest()


# In[ ]:




