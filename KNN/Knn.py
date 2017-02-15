# -*- coding: gb18030 -*-
from numpy import *
import math

#从CSV中读取数据，并把它们分割成训练数据集和测试数据集。
#相似度：计算两个数据实例之间的距离。
#临近：确定最相近的N个实例。
#结果：从这些实力中生成预测结果。
#准确度：总结预测的准确度。
#主程序：把这些串起来

def loadDataSet(fileName):
    frTrain = open(fileName);
    tainingSet = []
    for line in frTrain.readlines():
        currLine = line.strip().split(',')
        for i in range(3):
            tainingSet.append(currLine[i])
    return tainingSet

def eucl(ins1,ins2,length):
    distance=0
    for x in range(length):
        distance += pow((ins1[x]-ins2[x]),2)
    return math.sqrt(distance)

def getAccuary(TestData,prediction):
    errorCount = 0;
    for i in range(len(TestData)):
        if TestData[i] == prediction[i]:
            errorCount += 1
    rightRate = 1.0 - (float(errorCount)/len(TestData))
    print("the rigth rate of this test is: %f" % rightRate)
    return rightRate

def getNeighbors(TrainData,TestInstance,k):
    distance=[]
    length = len(TestInstance)-1
    for x in range(len(TrainData)):
        dist=eucl(TestInstance,TrainData[x],length)
        distance.append((TrainData[x],dist))
    distance.sort(key = operator.itemgetter(1))
    negibors=[]
    for i in range(k):
        negibors.append(distance[i][0])
    return negibors

def main():
    prediction=[]
    TestData = loadDataSet('data/test.txt')
    TrainData = loadDataSet('data/train.txt')
    k=3
    for i in range(len(TestData)):
        neighbor = getNeighbors(TrainData,TestData[i],k)
        result = getResult(neighbor);
        prediction.append(result)
        print 'prediction:' + prediction
    accuary = getAccuary(TestData,prediction)
    print 'accuary----' + accuary


main()