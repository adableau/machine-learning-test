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
        fr.readlines())  # get the number of lines in the file  file.readlines()是把文件的全部内容读到内存，并解析成一个list
    returnMat = zeros((numberOfLines, numberOfFeature))  # prepare matrix to return  3代表数据集中特征数目###
    classLabelVector = []  # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()  # strip() 参数为空时，默认删除空白符（包括'\n', '\r',  '\t',  ' ')
        listFromLine = line.split(',')  # split 以什么为标准分割一次  分成数组中的每个元素
        returnMat[index, :] = listFromLine[0:numberOfFeature]
        # classLabelVector.append(int(listFromLine[-1]))   #append() 方法向列表的尾部添加一个新的元素
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



# 为了防止某个属性对结果产生很大的影响，所以有了这个优化，比如:10000,4.5,6.8 10000就对结果基本起了决定作用
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
