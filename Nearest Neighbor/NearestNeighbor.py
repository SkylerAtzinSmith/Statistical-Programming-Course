#////////////////////////////////////////////////////////////////////////////////////////////////////																							
# Name:                  Skyler Smith
# Date:                  20-Sep-2020
# Course Name:			DATA 51100 | Statistical Programming										
# Semester:				Fall I 2020																
# Assignment Name:		PROGRAMMING ASSIGNMENT #3													
# Program Name:			Nearest Neighbor																																										
#////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------------------------
# This program classifies a testing set using Nearest-Neighbor algorithm and reports accuracy				
#----------------------------------------------------------------------------------------------------
#////////////////////////////////////////////////////////////////////////////////////////////////////

# import numpy
import numpy as np

# calculates the difference between 2 values and squares them    
def diffCalc(trVal, teVal):
    return (teVal-trVal)**2

# looks up the classifier for a certain index from a classifier mapping
def classify(classIndex, trainMapping):
        classifier = trainMapping[classIndex]
        return classifier

def accuracy_reporter(trueClass, predClass):
    if trueClass == predClass:
        return 1
    else:
        return 0
    
def printresults(number, trueClass, predClass):
    print(str(number)+","+str(trueClass)+","+str(predClass))
    
# Print Author Info
print("DATA-51100, Fall I 2020")
print("NAME: Skyler Smith")
print("PROGRAMMING ASSIGNMENT #3\n")

# import training data and testing data into 2D arrays of values and 1D arrays of classifiers
trainData = np.loadtxt("iris-training-data.csv", delimiter=",", usecols=[0, 1, 2, 3])
testData = np.loadtxt("iris-testing-data.csv", delimiter=",", usecols=[0, 1, 2, 3])
trainClasses = np.loadtxt("iris-training-data.csv", delimiter=",", usecols=[4], dtype=str)
testClasses = np.loadtxt("iris-testing-data.csv", delimiter=",", usecols=[4], dtype=str)

#index the training classifiers
trainMap = {key: val for key, val in enumerate(trainClasses)}

# make a holder for the distance matrix
distmat = np.zeros ((trainData.shape[0],testData.shape[0]))

# make a distance matrix for the testing data vs training data using vectorized functions
# use loop to stop the vectorized functions from doing pairwise calculation
# calculate distance to each training neighbor for entire set of testing values
# sum the the rows, then take the square root of those sums, resulting distData is a column of distances
# record the distances into the distance matrix column by column


distmat = np.sqrt((np.square(testData[:,np.newaxis]-trainData)).sum(axis=2))



# find the closest training neighbor, and return the corresponding index for the closest neighbor
Mindexes = distmat.argmin(axis = 1)

# vectorize the classify function
# lookup the classifier for the closest neighbors index, and returns the classifier for that neighbor
vclass = np.vectorize(classify)
classified = vclass(Mindexes, trainMap)

#vectorize accuracy reporter, then calculate the accuracy for the classification
vreport = np.vectorize(accuracy_reporter)
report = vreport(classified, testClasses)
acc = round(((np.sum(report)/report.size)*100), 2)

# generate a list for results, vectorize the printing function, and print the results
lister = np.arange(report.size) + 1
vprint = np.vectorize(printresults, otypes=[dict])

print('#, True, Predicted')
vprint(lister, testClasses, classified)
print('Accuracy: '+str(acc)+'%')







