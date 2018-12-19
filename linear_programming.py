from lpsolve55 import *
import numpy as np
import time, os
import multiprocessing as mp

class Worker(mp.Process):
    def __init__(self, inQ, outQ):
        super(Worker, self).__init__(target=self.start)
        self.inQ = inQ
        self.outQ = outQ

    def run(self):
        pass

class Graph(object):
    def __init__(self, vex, edge):
        self.vex = vex # 节点数量
        self.edge = edge # 边数量
        self.adj = np.zeros(shape=(self.edge,self.vex)) # 边行，节点数列
        np.random.seed(0)
        self.weight = np.random.rand(self.vex)*100 # 节点权重

def randomGraph(vex, edge):
    graph = Graph(vex, edge)
    for e in range(graph.edge):
        v0, v1 = 0, 0
        while v0 == v1:
            v0 = np.random.randint(0, graph.vex)
            v1 = np.random.randint(0, graph.vex)
        graph.adj[e, v0] = 1
        graph.adj[e, v1] = 1
    # with open("randGraph\\vex%sedge%s.randgraph" %(str(vex), str(edge)), 'x') as f:
    #     f.write("%s %s\n" %(str(vex), str(edge)))
    #     f.write("%s\n" %(str(graph.weight.tolist())))
    #     for e in range(graph.edge):
    #         v0, v1 = [v for v in range(graph.vex) if graph.adj[e, v] == 1]
    #         f.write("%s %s\n" %(str(v0), str(v1)))
    return graph

def randomRecGraph():
    pass

def randomCirGraph(vex, edge = None):
    if edge==None:
        edge = vex
    elif edge<vex:
        print("error on number of circle edges")
        exit(-2)
    graph = Graph(vex, edge)
    # 形成环路图
    for e in range(graph.vex):
        graph.adj[e, e % graph.vex] = 1
        graph.adj[e, (e+1) % graph.vex] = 1
    # 随机生成其他的边
    for e in range(graph.vex, graph.edge):
        v1, v1 = 0, 0
        while v0 == v1 or v0 == v1+1 or v0 == v1-1:
            v0 = np.random.randint(0, graph.vex)
            v1 = np.random.randint(0, graph.vex)
        graph.adj[e, v0] = 1
        graph.adj[e, v1] = 1
    # with open("randGraph\\vex%s.randcircle" %(str(vex)), 'x') as f:
    #     f.write("%s %s\n" %(str(vex), str(edge)))
    #     f.write("%s\n" %(str(graph.weight.tolist())))
    #     for e in range(graph.edge):
    #         v0, v1 = [v for v in range(graph.vex) if graph.adj[e, v] == 1]
    #         f.write("%s %s\n" %(str(v0), str(v1)))
    return graph

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

def linear_vex_cover(graph, filename, set_int = False, relax = False):
    t_start = time.time()
    lp = lpsolve("make_lp", 0, graph.vex)
    lpsolve("set_verbose", lp, IMPORTANT)
    ret = lpsolve("set_obj_fn", lp, graph.weight)
    for con in graph.adj:
        ret = lpsolve("add_constraint", lp, con, GE, 1)
    ret = lpsolve("set_lowbo", lp, [0 for i in range(graph.vex)])
    ret = lpsolve("set_upbo", lp, [1 for i in range(graph.vex)])
    # 如果是整数规划
    if set_int == True:
        for i in range(graph.vex):
            ret = lpsolve("set_int", lp, i+1, True)
    for i in range(graph.vex):
        ret = lpsolve('set_col_name', lp, i+1, "x"+str(i+1))
    filename += 'IP' if set_int == True else 'LP'
    # ret = lpsolve("write_lp", lp, filename+'.lp')
    lpsolve("solve", lp)
    x, ret = lpsolve('get_variables', lp)
    obj = lpsolve('get_objective', lp)
    print('x: ', x)
    print('obj: ', obj)
    print("time using: %s" %(time.time()-t_start))
    lpsolve("delete_lp", lp)
    if relax:
        for i in range(len(x)):
            if i>=0.5:
                x[i] = 1
            else:
                x[i] = 0
    result = []
    result.append('x:' + str(x))
    result.append('obj: ' + str(obj))
    result.append('time using: ' + str(time.time() - t_start))
    return result, filename+".lpg"

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
    filename = "randGraph\\vex%sedge%s.randcircle.pricing" %(str(graph.vex), str(graph.edge))
    return result, filename

def test():
    graph = Graph(4, 5)
    graph.adj = np.array([[1,1,0,0],
                          [1,0,1,0],
                          [1,0,0,1],
                          [0,1,1,0],
                          [0,0,1,1]])
    graph.weight = np.array([2,4,9,2])
    return graph

def task(filename, set_int = True):
    print('task: %s' %(os.getpid()), filename)
    graph = getdata(filename)
    result, write = linear_vex_cover(graph, filename, set_int)
    setdata(write, result)
    print('task: %s finished' %(os.getpid()))

def generateGraph():
    randname = []
    randGraph = []
    circlename = []
    circleGraph = []
    vertex = [10, 100, 1000]
    edge = []
    for v in vertex:
        edge.append(np.random.randint(0, v * (v - 1) / 2))
    for v, e in zip(vertex, edge):
        # 产生图类型
        filename = "randGraph\\vex%sedge%s.randgraph" % (str(v), str(e))
        graph = randomGraph(v, e)
        result, file = linear_vex_cover(graph, filename, set_int=False, relax=True)
        setdata(file, result)
        print(result)
        result, file = pricing_method(graph)
        setdata(file, result)
        print(result)

        filename = "randGraph\\vex%s.randcircle" % (str(v))
        graph = randomCirGraph(v)
        result, file = linear_vex_cover(graph, filename, set_int=False, relax=True)
        setdata(file, result)
        print(result)
        result, file = pricing_method(graph)
        setdata(file, result)
        print(result)

if __name__ == '__main__':
    generateGraph()
