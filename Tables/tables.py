#////////////////////////////////////////////////////////////////////////////////////////////////////																							
#Name:                  Skyler Smith
#Date:                  16-Oct-2020
#Course Name:			DATA 51100 | Statistical Programming										
#Semester:				Fall I 2020																
#Assignment Name:		PROGRAMMING ASSIGNMENT #7													
#Program Name:			tables.py																																										
#////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------------------------
# This program calculates aggregate statistics of PUMS data
#----------------------------------------------------------------------------------------------------
#////////////////////////////////////////////////////////////////////////////////////////////////////

#import pandas
import pandas as pd

# load a file into DataFrame
def load(filepath):
    data = pd.read_csv(filepath)
    return data

#def clean(df):
    
# Collect HH Type Data values and labels
def HHTlabel(data):
    famType = data['HHT'].unique()
    famType.sort()

    indx = []
    labels = []

    for i in range(1, len(famType) + 1):
        if i == 1:
            indx.append(i)
            labels.append('Married couple household')
        elif i == 2:
            indx.append(i)
            labels.append('Other family household:Male householder, no wife present')
        elif i == 3:
            indx.append(i)
            labels.append('Other family household:Female householder, no husband present')
        elif i == 4:
            indx.append(i)
            labels.append('Nonfamily household:Male householder:Living alone')
        elif i == 5:
            indx.append(i)
            labels.append('Nonfamily household:Male householder:Not living alone')
        elif i == 6:
            indx.append(i)
            labels.append('Nonfamily household:Female householder:Living alone')
        elif i == 7:
            indx.append(i)
            labels.append('Nonfamily household:Female householder:Not living alone')

    HTTdict = dict(zip(indx, labels))
    data.HHT = data.HHT.map(HTTdict)

# Collect HH Language Data values and labels
def HHLlabel(data):
    
    data['HHL'].dropna(inplace = True)
    lang = data['HHL'].unique()
    lang.sort()

    indx = []
    labels = []

    for i in range(1, len(lang) + 1):
        if i == 1:
            indx.append(i)
            labels.append('English only')
        elif i == 2:
            indx.append(i)
            labels.append('Spanish')
        elif i == 3:
            indx.append(i)
            labels.append('Other Indo-European languages')
        elif i == 4:
            indx.append(i)
            labels.append('Asian and Pacific Island languages')
        elif i >= 5:
            indx.append(i)
            labels.append('Other language')
      
    HHLdict = dict(zip(indx, labels))
    data.HHL = data.HHL.map(HHLdict)

# Label ACCESS values 
def ACCESSlabel(data):
    
    data['ACCESS'].dropna(inplace = True)
    ACC = data['ACCESS'].unique()  
    ACC.sort()

    indx = []
    labels = []

    for i in range(1, len(ACC) + 1):
        if i == 1:
            indx.append(i)
            labels.append('Yes w/ Subsrc.')
        elif i == 2:
            indx.append(i)
            labels.append('Yes, wo/ Subsrc.')
        elif i == 3:
            indx.append(i)
            labels.append('No')

    ACCdict = dict(zip(indx, labels))
    data.ACCESS = data.ACCESS.map(ACCdict)

# print Agg descriptive statistics in data1 table format
def table1(data, attribute_col, grouping_col, title):
   
   # Change the name of the column to match output if the grouping_col is HHT 
   if grouping_col == 'HHT':
       data.rename(columns = {'HHT':'HHT - Household/family type'}, inplace = True)
       grouping_col = 'HHT - Household/family type'
       
   # make a groupby object from atrribute and grouping attribute
   grouped = data[attribute_col].groupby(data[grouping_col])

   # describe the groupby object, drop other cols, save count, and reinsert in position 2
   tab1 = grouped.describe().drop(['25%', '50%', '75%'], axis = 1)
   tab1ct = tab1['count']
   tab1 = tab1.drop('count', axis=1)
   tab1.insert(loc=2, column = 'count', value=tab1ct)
    
   # format function to remove decimals from min & max & count
   fmt = lambda x: "{0:.0f}".format(x)
    
   # apply formatting
   tab1['min'] = tab1['min'].apply(fmt)
   tab1['max'] = tab1['max'].apply(fmt)
   tab1['count'] = tab1['count'].apply(fmt)
   
   # Sort by mean value
   tab1.sort_values(by=['mean'], ascending=False, inplace=True)
   
   # Output
   print(title)
   print (tab1)
   print('\n')
    
# print grouped agg statistics in table2 format
def table2(data, value_col, group_col1, group_col2, title):

    # Change the name of the column to match output if the grouping_col is HHL 
   if group_col1 == 'HHL':
       data.rename(columns = {'HHL':'HHL - Household language'}, inplace = True)
       group_col1 = 'HHL - Household language'
       
   # Create the crosstab dataframe    
   xTab = pd.crosstab(index=data[group_col1], values=data[value_col], aggfunc='sum', columns=data[group_col2], margins=True, normalize='all')

   #Move the first column to position at col index 2
   xTabct = xTab.iloc[:, 0]
   label = xTab.columns[0]
   xTab = xTab.drop(xTab.columns[0], axis = 1)
   xTab.insert(loc=2, column = label, value=xTabct)
       
   # Format function to make DF values as % with 2 decimals
   fmt = lambda x: "{0:.2f}%".format(x*100)
   
  
   # take the All row out, sort by the first column, then put back the All row at bottom
   insrow = xTab.loc['All']
   xTab = xTab.drop(['All'], axis = 0)
   xTab.sort_values(by=str(xTab.columns[0]), ascending = False, inplace = True)
   xTab = xTab.append(insrow)

   # Apply formatting to all values in the DF
   xTab = xTab.applymap(fmt)
   
   # Print titles and crosstable
   print(title)
   print('\t'*12+'sum')
   print('\t'*12+value_col)
   print(xTab)
   print('\n')
       
# quantile analysis table of aggregate data
def quantab3(data, qn, group_col, metric, title):
    
    print(title)

    # Make n number of groupings of equal size, drop nas, make a dict for ease of displaying 3q analysis
    grouping = pd.qcut(data[group_col], qn)
    q3 = ['low', 'medium', 'high']
    grouping.dropna(inplace = True)
    
    # rename the groups Lo, Med, Hi if using 3q analysis
    if qn == 3:
        d3=dict(zip(grouping.unique(),q3))
        grouping=grouping.map(d3)
    
    #group data into quantiles and get descriptive stats
    grouped = data[group_col].dropna().groupby(grouping)
    quantab = grouped.describe()

    # drop the stats we dont care about
    quantab = quantab.drop(['25%', '50%', '75%', 'count','std'], axis = 1)

    #Move the first column to position at col index 2
    quantabct = quantab.iloc[:, 0]
    label = quantab.columns[0]
    quantab = quantab.drop(quantab.columns[0], axis = 1)
    quantab.insert(loc=2, column = label, value=quantabct)

    # put qunatile attribute into main dataframe    
    data['bucket']=grouping

    # Name the columnb appropriately if the added metric is WGTP
    if metric == 'WGTP':
        colname = 'household_count'
    else: 
        colname = str(metric)
    
    # group added metric by quantile and add to output table
    quantab[colname] = data[metric].dropna().groupby(data['bucket']).sum()

    # Print the table
    print(quantab)
    print('\n')



# Make tables full display
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
   
# Print Author Info
print("DATA-51100, Fall I 2020")
print("NAME: Skyler Smith")
print("PROGRAMMING ASSIGNMENT #7\n")

# Load data into dataframe called data
data = load('ss13hil.csv')

# label HHL data and ACCESS Data
HHTlabel(data)
HHLlabel(data)
ACCESSlabel(data)
data['WGTP'].dropna(inplace = True)
data['HINCP'].dropna(inplace = True)

# Print descriptive stats of a grouping
table1(data, 'HINCP', 'HHT', '*** Table 1 - Descriptive Statistics of HINCP, grouped by HHT ***')

# Print a dual grouping frequnecy table
table2(data, 'WGTP', 'HHL', 'ACCESS', "*** Table 2 - HHL vs. ACCESS - Frequency Table ***")

# print quanntile analysis table
quantab3(data, 3, 'HINCP', 'WGTP', '*** Table 3 - Quantile Analysis of HINCP - Household income (past 12 months) ***')





