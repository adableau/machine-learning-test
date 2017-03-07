# -*- coding: utf-8 -*-

from pygraph.classes.digraph import digraph


class PRIterator:
    __doc__ = '''计算的web-google的PR值'''

    def __init__(self, dg):
        self.damping_factor = 0.85  # 阻尼系数,即α
        self.max_iterations = 100  # 最大迭代次数
        self.min_delta = 0.00001  # 确定迭代是否结束的参数,即ϵ
        self.graph = dg

    def page_rank(self):
        #  先将图中没有出链的节点改为对所有节点都有出链
        for node in self.graph.nodes():
            if len(self.graph.neighbors(node)) == 0:
                for node2 in self.graph.nodes():
                    digraph.add_edge(self.graph, (node, node2))
        print '------------------'
        nodes = self.graph.nodes()
        graph_size = len(nodes)
        print graph_size
        if graph_size == 0:
            return {}
        page_rank = dict.fromkeys(nodes, 1.0 / graph_size)  # 给每个节点赋予初始的PR值
        damping_value = (1.0 - self.damping_factor) / graph_size  # 公式中的(1−α)/N部分

        flag = False
        for i in range(self.max_iterations):
            print("This is NO.%s iteration" % (i + 1))
            change = 0
            for node in nodes:
                rank = 0
                for incident_page in self.graph.incidents(node):  # 遍历所有“入射”的页面
                    rank += self.damping_factor * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                rank += damping_value
                change += abs(page_rank[node] - rank)  # 绝对值
                page_rank[node] = rank
            if change < self.min_delta:
                flag = True
                break
        if flag:
            print("finished in %s iterations!" % node)
        else:
            print("finished out of 100 iterations!")
        return page_rank


def loadDataSet(dataFileName):
    dg = digraph()
    # dg.add_nodes(["A", "B", "C", "D", "E"])
    # dg.add_edge(("A", "B"))
    data_nodes = []
    data_nodes_list = []
    print "-----add_nodes---------"
    fr = open(dataFileName)
    for line in fr:
        if "#" not in line.lower():
            lineArr = line.strip().split()  # 0	11342
            data_nodes.append(lineArr[0])
            data_nodes.append(lineArr[1])
            str = (lineArr[0], lineArr[1])
            data_nodes_list.append(str)
    data_node = {}.fromkeys(data_nodes).keys()
    dg.add_nodes(data_node)
    print "-----add_edge---------"
    print len(data_nodes_list)
    for line in data_nodes_list:
        print line
        dg.add_edge(line)
    return dg


if __name__ == '__main__':
    print "--start----------------------"
    dg = loadDataSet("web-Google.txt")
    print "--down---loadDataSet---------"
    pr = PRIterator(dg)
    print "--down---PRMapReduce---------"

    page_ranks = pr.page_rank()
    print "-----PageRank---------"
    #  排序PageRank
    dict = sorted(page_ranks.iteritems(), key=lambda d: d[1], reverse=True)
    print dict[0]
    print dict[1]
    print dict[2]
    # print("The final page rank is\n", page_ranks)
