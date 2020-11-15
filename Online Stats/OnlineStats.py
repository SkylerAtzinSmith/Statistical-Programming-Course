#////////////////////////////////////////////////////////////////////////////////////////////////////																							
#Name:                  Skyler Smith
#Date:                  05-Sep-2020
#Course Name:			DATA 51100 | Statistical Programming										
#Semester:				Fall I 2020																
#Assignment Name:		PROGRAMMING ASSIGNMENT #1													
#Program Name:			OnlineStats																																										
#////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------------------------
# This program generates the mean and variance for user input in realtime					
#----------------------------------------------------------------------------------------------------
#////////////////////////////////////////////////////////////////////////////////////////////////////

#Print Author Info
print("DATA-51100, Fall I 2020")
print("NAME: Skyler Smith")
print("PROGRAMMING ASSIGNMENT #1")

#ask for first number input
num = float(input("Enter a number: "))

#Define Variables for n, mean will be the number enetered & variance will be 0 for the first entry
#looper variable will be true to keep the loop going until a negative is entered
n = 1
mean = num
var = float(0)
looper = True

#Only report values of a positive number or 0 is enetered
if mean >= 0:
    #Print the first line of stats
    print ("Mean is " + str(mean) + " " + "variance is " + str(var))
else:
    looper = False

#for the next entries n will be > 1. Stops looping once a negative number is entered
while looper == True:
    
    #get a new num
    num = float(input("Enter a number: "))
    
    #as long as the new num >= 0, the stats are calculated and reported
    if num >= 0:
    
        n = n + 1
    
        var = ((n-2)/(n-1))*var + ((num-mean)*(num-mean))/n
        
        mean = mean + (num-mean)/n
    
        print ("Mean is " + str(mean) + " " + "variance is " + str(var))
   
    #once a negative number is entered, the looper changes to false
    if num < 0:
        looper = False
     
    
    