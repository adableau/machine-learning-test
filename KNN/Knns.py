# -*- coding: gb18030 -*-
from numpy import *
import operator

# KNN���㷨���ľ���ŷʽ����ļ��㣬һ�������Ǽ��������ĵ��ѵ�����е���һ���ŷʽ����

def classify(inMat, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inMat, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    distance = sqDiffMat.sum(axis=1) ** 0.5
    # ��������һЩͳ�ƹ���
    sortedDistIndicies = distance.argsort()
    classCount = {}
    for i in range(k):
        labelName = labels[sortedDistIndicies[i]]
        classCount[labelName] = classCount.get(labelName, 0) + 1;
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


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
        else:
            # elif listFromLine[-1] == 'Iris-virginica' :
            classLabelVector.append(3)
        index += 1
    return returnMat, classLabelVector


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
    trianingMat, classLabel = file2Mat(trainigSetFileName, 3)
    trianingMat, minVals, ranges = autoNorm(trianingMat)
    testMat, testLabel = file2Mat(testFileName, 3)
    testSize = testMat.shape[0]
    errorCount = 0.0
    for i in range(testSize):
        result = classify((testMat[i] - minVals) / ranges, trianingMat, classLabel, 3)
        if (result != testLabel[i]):
            errorCount += 1.0
    errorRate = errorCount / (float)(len(testLabel))
    return errorRate;


if __name__ == "__main__":
    errorRate = test('data/test.txt', 'data/train.txt')
    print("the error rate is :%f" % (1- errorRate))