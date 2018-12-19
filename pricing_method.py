import numpy as np
import copy as cp
import time

class Graph(object):
    def __init__(self, vex, edge):
        self.vex = vex # 节点数量
        self.edge = edge # 边数量
        self.adj = np.zeros(shape=(self.edge,self.vex)) # 边行，节点数列
        np.random.seed(0)
        self.weight = np.random.rand(self.vex)*100 # 节点权重

def getdata(filename):
    with open(filename, 'r') as f:
        vex, edge = map(int, f.readline().strip().split(' '))
        graph = Graph(vex, edge)
        for line, i in zip(f.readlines(), range(edge)):
            v1, v2= map(int, line.strip().split(' ')[:2])
            graph.adj[i, v1], graph.adj[i,v2] = 1, 1
    return graph

def setdata(filename, result):
    with open(filename, 'w') as f:
        for rsl in result:
            f.write('/*'+rsl+'*/\n')


def pricing_method(graph):
    start = time.time()
    result = []
    tight_nodes = graph.weight
    covered_edges = np.zeros(graph.edge)
    p = np.zeros_like(graph.adj)
    for i in range(graph.edge):
        if covered_edges[i]==1:
            continue
        # 还没被cover
        ver = [j for j in range(graph.vex) if graph.adj[i][j]==1]
        _min = min(tight_nodes[ver[0]], tight_nodes[ver[1]])
        tight_nodes[ver[0]] -= _min
        tight_nodes[ver[1]] -= _min
        if tight_nodes[ver[0]] == 0:
            for j in range(graph.edge):
                if graph.adj[j,ver[0]] == 1:
                    covered_edges[j] = 1
        if tight_nodes[ver[1]] == 0:
            for j in range(graph.edge):
                if graph.adj[j,ver[1]] == 1:
                    covered_edges[j] = 1
    for i in range(len(tight_nodes)):
        if tight_nodes[i] != 0:
            tight_nodes[i] = 0
        else:
            tight_nodes[i] = 1
    result.append('x: ' + str(tight_nodes))
    result.append('obj: ' + str(np.dot(tight_nodes, graph.weight)))
    result.append('time using: ' + str(time.time()-start))
    return result


def tight(graph, vex):
    tight_nodes = []
    for j in range(graph.edge):
        if graph.adj[j, vex] == 1:
            tight_nodes.append(j)
    return tight_nodes

def test():
    graph = Graph(4, 5)
    graph.adj = np.array([[1,1,0,0],
                          [1,0,1,0],
                          [1,0,0,1],
                          [0,1,1,0],
                          [0,0,1,1]])
    graph.weight = np.array([2,4,9,2])
    return graph

if __name__ == '__main__':
    randg = ["randGraph\\vex10edge0.randgraph", "randGraph\\vex100edge3049.randgraph", "randGraph\\vex1000edge482721.randgraph"]
    randc = ["randGraph\\vex10edge10.randcircle", "randGraph\\vex100edge100.randcircle", "randGraph\\vex1000edge1000.randcircle", "randGraph\\vex10000edge10000.randcircle"]
    for file in filename:
        graph = getdata(file)
        result = pricing_method(graph)
        setdata(file+"pricing.txt", result)
        print(result)