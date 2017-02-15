#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Code:Create by Ada
#PCA
from sklearn.decomposition import PCA
from pylab import plot, show
from numpy import *


def loadDataSet(fileName):
    fr = open(fileName)
    #读数据
    stringArr = fr.readlines();
    # read the first 4 columns
    data = genfromtxt(stringArr,delimiter=',',usecols=(0,1,2,3))
    # read the fifth column
    target = genfromtxt(stringArr,delimiter=',',usecols=(4),dtype=str)
    #print set(target)

    #实例化PCA
    pca = PCA(n_components=2)
    pcad = pca.fit_transform(data)
    plot(pcad[target=='Iris-setosa',0],pcad[target=='Iris-setosa',1],'bo')
    plot(pcad[target=='Iris-versicolor',0],pcad[target=='Iris-versicolor',1],'ro')
    plot(pcad[target=='Iris-virginica',0],pcad[target=='Iris-virginica',1],'go')


    #查看主成分PC
    print pca.explained_variance_ratio_
    #output: [ 0.92461621  0.05301557]
    pc1, pc2 = pca.explained_variance_ratio_ #保存2个PC

    print 1-sum(pca.explained_variance_ratio_)
    #output:0.0223682249752
    print 1.0-pc1-pc2 #等价于上述输出

    #逆变换还原数据
    data_inv = pca.inverse_transform(pcad)
    #比较还原后数据和原始数据的相似度
    print abs(sum(sum(data - data_inv)))
    #output:6.66133814775e-15

    #循环尝试：PC数量从1维到4维（原始数据也是4维）
    #看PCA覆盖信息量；4个肯定100%，3个也很高了；
    for i in range(1,5):
        pca = PCA(n_components=i)
        pca.fit(data)
        print sum(pca.explained_variance_ratio_) * 100,'%'
    #显示
    show()

if __name__=='__main__':
    loadDataSet('iris.data.txt')

