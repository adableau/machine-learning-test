# coding=utf-8
# python edition: Python3.4.1,2014,9,24
from collections import defaultdict
from random import uniform
from math import sqrt


def read_points():
    dataset = []
    with open('data/kmeans/irisNoLabel.data', 'r') as file:
        for line in file:
            if line == '\n':
                continue
            dataset.append(list(map(float, line.split(','))))
        file.close()
        return dataset


def write_results(listResult, dataset, k):
    with open('data/kmeans/result.txt', 'a') as file:
        for kind in range(k):
            file.write("\nCLASSINFO:%d\n" % (kind + 1))
            for j in listResult[kind]:
                line = str(dataset[j]) + "," + str(j)
                print line
                file.write(line)
                file.write('\n')
        file.close()


def point_avg(points):
    dimensions = len(points[0])
    new_center = []
    for dimension in range(dimensions):
        sum = 0
        for p in points:
            sum += p[dimension]
        new_center.append(float("%.8f" % (sum / float(len(points)))))
    return new_center


def update_centers(data_set, assignments, k):
    new_means = defaultdict(list)
    centers = []
    for assignment, point in zip(assignments, data_set):
        new_means[assignment].append(point)
    for i in range(k):
        points = new_means[i]
        centers.append(point_avg(points))
    return centers


def assign_points(data_points, centers):
    assignments = []
    for point in data_points:
        shortest = float('inf')
        shortest_index = 0
        for i in range(len(centers)):
            value = distance(point, centers[i])
            if value < shortest:
                shortest = value
                shortest_index = i
        assignments.append(shortest_index)
    if len(set(assignments)) < len(centers):
        print "--1--\n"
        exit()
    return assignments


def distance(a, b):
    dimention = len(a)
    sum = 0
    for i in range(dimention):
        sq = (a[i] - b[i]) ** 2
        sum += sq
    return sqrt(sum)


def generate_k(data_set, k):
    centers = []
    dimentions = len(data_set[0])
    min_max = defaultdict(int)
    for point in data_set:
        for i in range(dimentions):
            value = point[i]
            min_key = 'min_%d' % i
            max_key = 'max_%d' % i
            if min_key not in min_max or value < min_max[min_key]:
                min_max[min_key] = value
            if max_key not in min_max or value > min_max[max_key]:
                min_max[max_key] = value
    for j in range(k):
        rand_point = []
        for i in range(dimentions):
            min_val = min_max['min_%d' % i]
            max_val = min_max['max_%d' % i]
            tmp = float("%.8f" % (uniform(min_val, max_val)))
            rand_point.append(tmp)
        centers.append(rand_point)
    return centers


def k_means(dataset, k):
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments, k)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    result = list(zip(assignments, dataset))
    # for out in result :
    print '--------------------------------result--------------------------------------\n\n'
    listResult = [[] for i in range(k)]
    count = 0
    for i in assignments:
        listResult[i].append(count)
        count = count + 1
    write_results(listResult, dataset, k)
    for kind in range(k):
        print "第%d类数据有:" % (kind + 1)
        count = 0
        for j in listResult[kind]:
            count = count + 1
            if count % 25 == 0:
                print '\n'
    print '\n\n--------------------------------end------------------------------------------------\n\n'


def main():
    dataset = read_points()
    k_means(dataset, 3)


if __name__ == "__main__":
    main()
