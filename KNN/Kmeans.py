# -*- coding: gb18030 -*-
from numpy import *
import math
import matplotlib.pyplot as plt


# calculate Euclidean distance
def euclDistance(vector1, vector2):
    return sqrt(sum(power(vector2 - vector1, 2)))


# init centroids with random samples
def initCentroids(dataSet, k):
    numSamples, dim = dataSet.shape
    centroids = zeros((k, dim))
    for i in range(k):
        index = int(random.uniform(0, numSamples))
        centroids[i, :] = dataSet[index, :]
    return centroids


# k-means cluster
def kmeans(dataSet, k):
    numSamples = dataSet.shape[0]
    # first column stores which cluster this sample belongs to,
    # second column stores the error between this sample and its centroid
    clusterAssment = mat(zeros((numSamples,4)))
    clusterChanged = True

    ## step 1: init centroids
    centroids = initCentroids(dataSet, k)

    while clusterChanged:
        clusterChanged = False
        ## for each sample
        for i in xrange(numSamples):
            minDist = 100000.0
            minIndex = 0
            ## for each centroid
            ## step 2: find the centroid who is closest
            for j in range(k):
                distance = euclDistance(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist = distance
                    minIndex = j
             ## step 3: update its cluster
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
                clusterAssment[i, :] = minIndex, minDist ** 2

                ## step 4: update centroids
        for j in range(k):
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
            centroids[j, :] = mean(pointsInCluster, axis=0)
    print 'Congratulations, cluster complete!'
    return centroids, clusterAssment


def file2Mat(filename,numberOfFeature):
    fr = open(filename)
    numberOfLines = len(
        fr.readlines())  # get the number of lines in the file  file.readlines()�ǰ��ļ���ȫ�����ݶ����ڴ棬��������һ��list
    returnMat = zeros((numberOfLines, numberOfFeature))  # prepare matrix to return  3�������ݼ���������Ŀ###
    classLabelVector = []  # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()  # strip() ����Ϊ��ʱ��Ĭ��ɾ���հ׷�������'\n', '\r',  '\t',  ' ')
        listFromLine = line.split(',')  # split ��ʲôΪ��׼�ָ�һ��  �ֳ������е�ÿ��Ԫ��
        returnMat[index, :] = listFromLine[0:numberOfFeature]
        # classLabelVector.append(int(listFromLine[-1]))   #append() �������б��β�����һ���µ�Ԫ��
        if listFromLine[-1] == 'Iris-setosa':
            classLabelVector.append(1)
        elif listFromLine[-1] == 'Iris-versicolor':
            classLabelVector.append(2)
        elif listFromLine[-1] == 'Iris-virginica' :
            classLabelVector.append(3)
        index += 1
    return returnMat, classLabelVector


# show your cluster only available with 2-D data
def showCluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape

    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print "Sorry! Your k is too large! please contact Zouxy"
        return 1

        # draw all samples
    for i in xrange(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # draw the centroids
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)

    plt.show()



# Ϊ�˷�ֹĳ�����ԶԽ�������ܴ��Ӱ�죬������������Ż�������:10000,4.5,6.8 10000�ͶԽ���������˾�������
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normMat = zeros(shape(dataSet))
    size = normMat.shape[0]
    normMat = dataSet - tile(minVals, (size, 1))
    normMat = normMat / tile(ranges, (size, 1))
    return normMat, minVals, ranges


def test(trainigSetFileName, testFileName):
    ## step 1: load data
    print "step 1: load data..."
    #trianingMat, classLabel = file2Mat(trainigSetFileName, 4)
    #trianingMat, minVals, ranges = autoNorm(trianingMat)
    testMat, testLabel = file2Mat(testFileName, 4)
    testSize = testMat.shape[0]

    print "step 2: clustering..."
    dataSet = mat(testMat)
    k = 3
    centroids, clusterAssment = kmeans(testMat, k)

    ## step 3: show the result
    print "step 3: show the result..."
    showCluster(dataSet, k, centroids, clusterAssment)

    errorCount = 0.0
    for i in range(testSize):
        result =kmeans(trianingMat,k)

      #result = classify((testMat[i] - minVals) / ranges, trianingMat, classLabel, 3)
        if (result != testLabel[i]):
            errorCount += 1.0
    errorRate = errorCount / (float)(len(testLabel))
    return errorRate;


if __name__ == "__main__":
    errorRate = test('data/kmeans/iris.data', 'data/kmeans/irisNoLabel.data')
    print("the error rate is :%f" % (1- errorRate))
