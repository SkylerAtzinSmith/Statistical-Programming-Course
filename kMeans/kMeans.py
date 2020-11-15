# Assignment 2

# printing header with course, name, assignment, and due date
print("Data 51100 - Fall 2020")
print("Group 3: Jacob Kerschner, Skyler Smith, and Daniel Zapotoczny")
print("Programming Assignment #2")
print("Sunday September 13th, 2020")

'''
This program uses k-means clustering to sort a
predetermined list of values into k clusters where
k comes from a user input.
'''


# function to calculate the mean of all elements in a list object
def meanCalc(list):
    mean = 0
    for i in range(0, len(list)):
        if i == 0:
            mean = list[0]
            n = 1
        else:
            n = n + 1
            mean = mean + ((list[i] - mean) / n)
    return mean


# make a dict mapping the means of each element in a cluster to cluster index
def mapMeans(k, clusters):
    meanDict = {}
    for i in range(0, k):
        mean = meanCalc(clusters[i])
        meanDict.update({i: mean})

    return meanDict


# recluster the values based on a set mean value for each cluster
def recluster(ogData, meanDict, k):
    newClusters = dict(zip(range(k), [[] for i in range(k)]))

    for x in ogData:

        shortestDist = float('inf')

        for i in range(0, k):

            dist = abs(x - meanDict[i])

            if dist < shortestDist:
                shortestDist = dist
                key = i

        newClusters[key].append(x)

    newMeanDict = mapMeans(k, newClusters)

    return newClusters, newMeanDict


# function to identify what is the key associated with an element from a list object value in a dict
def identifyclusters(x, finalClusters):
    for key in finalClusters:

        for val in finalClusters[key]:

            if x == val:
                return key


# open file and make data list object
path = "prog2-input-data-experiment.txt"
with open(path) as f:
    data = [float(x.rstrip()) for x in open(path)]

# close the file to save resources
f.close()

# save a copy of the original data list
ogData = data.copy()

# prompt user for number of clusters
k = int(input("Enter the number of clusters: "))

# prevent user from entering more k than existing values
while k > len(data):
    k = int(input("Enter the number of clusters: "))

# define first k values as the centroids
centroids = dict(zip(range(k), data[0:k]))

# make an empty list for each k
clusters = dict(zip(range(k), [[] for i in range(k)]))
old_point_assignments = {}

# put centroids into clusters
for i in range(0, k):
    clusters[i].append(centroids[i])

# calculate the mean of each cluster
meanDict = mapMeans(k, clusters)

# pop out the first k values from the dataset so you do not append duplicate values when clustering
for i in range(0, k):
    data.pop(0)

# for each element in the data list, find the cluster whos mean is the shortest distance away
# then append the element to that cluster, and recalculate the mean of the clusters.
for x in data:

    shortestDist = float('inf')

    for i in range(0, k):

        dist = abs(x - meanDict[i])

        if dist < shortestDist:
            shortestDist = dist
            key = i

    clusters[key].append(x)
    meanDict = mapMeans(k, clusters)

# Print the first iteration
print('')
print("Iteration 1")

for key in clusters:
    print(str(key) + " " + str(clusters[key]))
finalClusters = clusters
prevCluster = clusters
prevMeanDict = meanDict


# run and print the each subsequent iteration by loading the original dataset
# and the calculated mean for each cluster
for i in range(2, 1000):
    print("\nIteration", i)
    curClusters, curMeanDict = recluster(ogData, prevMeanDict, k)

    for key in curClusters:
        print(str(key) + " " + str(curClusters[key]))
    finalClusters = curClusters

    if curClusters == prevCluster:
        break
    prevCluster = curClusters
    prevMeanDict = curMeanDict

# Print the final results of the clustering
print('')
for x in ogData:
    print("point " + str(x) + " in cluster " + str(identifyclusters(x, finalClusters)))

# create file and write points and clusters to the output file
out_path = "prog2-output-data.txt"
with open(out_path, "w+") as f:
    for x in ogData:
        f.write("point " + str(x) + " in cluster " + str(identifyclusters(x, finalClusters)) + "\n")

# close the output file
f.close()