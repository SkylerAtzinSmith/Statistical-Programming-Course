#////////////////////////////////////////////////////////////////////////////////////////////////////																							
#Name:                  Skyler Smith
#Date:                  04-Oct-2020
#Course Name:			DATA 51100 | Statistical Programming										
#Semester:				Fall I 2020																
#Assignment Name:		PROGRAMMING ASSIGNMENT #5													
#Program Name:			DataStats																																										
#////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------------------------
# This program...ect.
#----------------------------------------------------------------------------------------------------
#////////////////////////////////////////////////////////////////////////////////////////////////////

# Print Author Info
print("DATA-51100, Fall I 2020")
print("NAME: Skyler Smith")
print("PROGRAMMING ASSIGNMENT #5\n")

# import numpy, ,pandas, DF & S Objects, and regular expressions package
import pandas as pd
from pandas import DataFrame
import re

# new function to determine the start time. adds the start time to the the other start time if multiple exist
def startTimeCounter(DF, referencecolumn, value, newcolumn):
    DF.loc[DF[str(referencecolumn)].str.contains(str(value)+':'), str(newcolumn)] = DF[str(newcolumn)]+int(value)
    

# read the csv file into a DataFrame object
data = DataFrame(data=pd.read_csv('cps.csv'))

#make a splitter function to read comma seperated values (like the all grades offered col)
splitter = lambda x : re.split(',', x)

# function to gather the lowest grade
mincaller = lambda x : x[0]

# function to gather the highest grade
maxcaller = lambda x : x[-1]

# Function to fillna with mean for columns (x) if dtype is int, unsigned int, float, or complex floating point, otherwise fill with 'N/A'
filler = lambda x : x.fillna(x.mean()) if x.dtype.kind in 'iufc' else x.fillna('N/A')

# fIll in all NAs, fills in numerics with column mean, fills in 'N/A' if not numeric column
data=data.apply(filler)

# make tuples of all grades offered, then put the lowest and highest into new columns using min and max caller functions
data['Lowest_Grade'] = data['Grades_Offered_All'].apply(splitter).apply(mincaller)
data['Highest_Grade'] = data['Grades_Offered_All'].apply(splitter).apply(maxcaller)


# Set a new column called starting hour to 0
data['School_Start_Hour'] = 0

# map counter to account for schools that conditionally start at different times
counter_map={7:7, 8:8, 9:9, 15:(7, 8), 16:(7, 9), 17:(8, 9)}

# run the statTimeCounter for 7, 8 , and 9.
startTimeCounter(data, 'School_Hours', 7, 'School_Start_Hour')
startTimeCounter(data, 'School_Hours', 8, 'School_Start_Hour')
startTimeCounter(data, 'School_Hours', 9, 'School_Start_Hour')

# apply the mapping for schools that start at different start times
data['School_Start_Hour']=data['School_Start_Hour'].map(counter_map)

# print output output tables
output=data[['School_ID', 'Short_Name', 'Is_High_School', 'Zip', 'Student_Count_Total', 'College_Enrollment_Rate_School', 'Lowest_Grade','Highest_Grade', 'School_Start_Hour']]
print(str(output.head(10)).replace('[10 rows x 9 columns]', ''))

# format stats for High School and Non-High School stats
hsStats=data[data['Is_High_School']==True].describe().round(2)
non_hsStats=data[data['Is_High_School']==False].describe().round(2)

# Print the required stats
print('College Enrollment Rate for High Schools = '+str(hsStats['College_Enrollment_Rate_School']['mean'])+' (sd='+str(hsStats['College_Enrollment_Rate_School']['std'])+')\n')
print('Total Student Count for non-High Schools = '+str(non_hsStats['Student_Count_Total']['mean'])+' (sd='+str(non_hsStats['Student_Count_Total']['std'])+')\n')

# Print the output, combine shared hours
print("Distribution of Starting Hours:")
print('8am: '+str(data['School_Start_Hour'].value_counts()[8]+data['School_Start_Hour'].value_counts()[(7, 8)]))
print('7am: '+str(data['School_Start_Hour'].value_counts()[7]+data['School_Start_Hour'].value_counts()[(7, 8)]+data['School_Start_Hour'].value_counts()[(7, 9)]))
print('9am: '+str(data['School_Start_Hour'].value_counts()[9]+data['School_Start_Hour'].value_counts()[(7, 9)]))

# Select only data outside of the zipcodes listed
selDat=data[~data['Zip']==('N/A')]
selDat=selDat[~selDat['Zip'].astype(str).str.contains('60601')]
selDat=selDat[~selDat['Zip'].astype(str).str.contains('60602')]
selDat=selDat[~selDat['Zip'].astype(str).str.contains('60603')]
selDat=selDat[~selDat['Zip'].astype(str).str.contains('60604')]
selDat=selDat[~selDat['Zip'].astype(str).str.contains('60605')]
selDat=selDat[~selDat['Zip'].astype(str).str.contains('60606')]
selDat=selDat[~selDat['Zip'].astype(str).str.contains('60607')]
selDat=selDat[~selDat['Zip'].astype(str).str.contains('60616')]

print('\nNumber of schools outside Loop: '+str(selDat['Zip'].count()))


