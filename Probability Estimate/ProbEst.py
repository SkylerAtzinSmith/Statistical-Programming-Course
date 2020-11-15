#////////////////////////////////////////////////////////////////////////////////////////////////////																							
#Name:                  Skyler Smith
#Date:                  27-Sep-2020
#Course Name:			DATA 51100 | Statistical Programming										
#Semester:				Fall I 2020																
#Assignment Name:		PROGRAMMING ASSIGNMENT #4													
#Program Name:			ProbEst																																										
#////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------------------------
# This program computes and displays conditional probability of car aspiration based on make			
#----------------------------------------------------------------------------------------------------
#////////////////////////////////////////////////////////////////////////////////////////////////////

    

# Print Author Info
print("DATA-51100, Fall I 2020")
print("NAME: Skyler Smith")
print("PROGRAMMING ASSIGNMENT #4\n")

# import pandas & DataFrame objects
import pandas as pd
from pandas import DataFrame

# read the csv file into a DataFrame object
data = DataFrame(data=pd.read_csv('cars.csv'))

# set the make to be the index values
data.set_index(['make'], drop = False, inplace = True)

# make a new DataFrame to hold the make probabilities, default for all = 0, also set make to index value to match data index
makeProb = DataFrame(data.index.unique())
makeProb.insert(1, column = 'makeProb', value=0)
makeProb.set_index(['make'], inplace=True)

# make a function to format everything to 2 decimal places and add % sign
format = lambda x: str(round(x, 2))+'%'

# loop to calculate the probabilities for each make and print the output
for i in data.index.unique():
    
    # counts is the number of std and number of turbo models. Returns a Series obj
    counts = pd.value_counts(data.loc[i]['aspiration'])
    
    # count number of std models. try-except for KeyError in case there is no 'Std' model, then use 0
    try:
        std = counts['std']
    except KeyError:
        std = 0
    
    # count the number of turbo models. try-except for KeyError in case there is no 'turbo' model, then use 0
    try:
        turbo = counts['turbo']
    except KeyError:
        turbo = 0
    
    # count the total number of models for the make
    total = std+turbo
    
    # calculate the probability of each model for the make and format
    probStd = format(std/total*100)
    probTurbo = format(turbo/total*100)
    
    # calculate the probability of each make and save it to the previously created DF
    makeProb.loc[i] = format(total/data.make.count()*100)
    
    # print the results for each model by make
    print("Prob(aspiration=std|make="+str(i)+") = "+str(probStd))
    print("Prob(aspiration=turbo|make="+str(i)+") = "+str(probTurbo))

# seperate the outputs
print('')
    
# loop to print the output of the make probability after outputting all the model probabilities by make
for i in makeProb.index:
    print("Prob(make=" + str(i) + ') = ' + str(makeProb.loc[i][0]))    

    