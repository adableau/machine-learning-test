# -*- coding: utf-8 -*-
"""
"""
import numpy as np
from sklearn import datasets

dataFileName = "Iris.txt"


# 读取训练数据
# #
def loadDataSet(dataFileName):
    dataMat = []
    fr = open(dataFileName)
    for line in fr:
        lineArr = line.strip().split()
        dataMat.append([float(lineArr[1]), float(lineArr[2]), float(lineArr[3]), float(lineArr[4])])
    return dataMat


def predict_targets(dataFileName):
    global clf
    # load the iris dataset
    irisDataset = datasets.load_iris()
    train_data = np.concatenate((irisDataset.data[0:40, :], irisDataset.data[50:90, :], irisDataset.data[100:140, :]),
                                axis=0)
    train_target = np.concatenate((irisDataset.target[0:40], irisDataset.target[50:90], irisDataset.target[100:140]),
                                  axis=0)
    test_data = loadDataSet(dataFileName)

    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier(criterion='gini')
    clf.fit(train_data, train_target)  # 训练决策树
    DecisionTreeClassifier(criterion='gini', max_depth=None, max_features=None,
                           min_samples_leaf=1, min_samples_split=2, random_state=None,
                           splitter='best')
    print len(test_data)
    predict_target = clf.predict(test_data)  # 预测
    print len(predict_target)
    save_iris(test_data, predict_target)
    return clf


def save_data(clf):
    from sklearn.tree import export_graphviz
    with open("iris.dot", 'w') as f:
        f = export_graphviz(clf, out_file=f)


def save_iris(test_data, predict_target):
    for line in range(len(test_data)):
        print line
        test_data[line].append(predict_target[line])
    f = open('irisdata.txt', 'w')
    f.write(str(test_data))
    f.close()


if __name__ == '__main__':
    clf = predict_targets(dataFileName)
    save_data(clf)
