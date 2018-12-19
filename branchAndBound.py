from pulp import *
import numpy as np
import copy as cp

'''分支定界法'''
# 剪枝条件
# 1.达到最大权重
# 2.上界等于下界
# 3.别的节点的上界小于等于当前最优解

class Item(object):
    def __init__(self, idx, value, weight):
        self.index = idx
        self.value = value
        self.weight = weight
        self.ratio = value/weight

class BBTreeNode(object):
    def __init__(self, items, cap, value):
        self.itemsToSelect = items
        self.capacity = cap
        self.value = value

    def setParent(self, par):
        self.parent = par

    def upperBound(self):
        # 创建线性规划问题
        prob = LpProblem("Knapsack Problem", LpMaximize)
        # 创建线性规划问题变量
        X = []
        for i in range(len(self.itemsToSelect)):
            var = "x"+str(i)
            X.append(LpVariable(var, lowBound=0, upBound=1))
        # 创建目标方程
        prob += lpSum([self.itemsToSelect[i].value*X[i] for i in range(len(self.itemsToSelect))])

        # 添加约束条件
        prob += lpSum([self.itemsToSelect[i].weight*X[i] for i in range(len(self.itemsToSelect))]) <=self.capacity
        # 解方程
        prob.solve()
        # 设置上界
        self.ub = self.value + sum([self.itemsToSelect[i].value*X[i].value() for i in range(len(self.itemsToSelect))])
        # 输出测试
        for x in prob.variables():
            print(x.name, " = ", x.varValue)

    def lowerBound(self):
        # 首先按照权值排序
        self.itemsToSelect.sort(key=lambda x:x.ratio, reverse=True)
        # 然后累加直到超过容量
        weight, value = 0, 0
        for i, item in enumerate(self.itemsToSelect):
            weight += item.weight
            value += item.value
            if(self.capacity < weight):
                weight -= item.weight
                value -= item.value
                break
        self.lb = self.value + value

    def acceptItem(self):
        leftChild_item = cp.deepcopy(self.itemsToSelect)
        item = leftChild_item.pop(0)
        leftChild_cap = self.capacity - item.weight
        leftChild_val = self.value + item.value
        self.leftChild = BBTreeNode(leftChild_item, leftChild_cap, leftChild_val)

    def rejectItem(self):
        rightChild_item = cp.deepcopy(self.itemsToSelect)
        del rightChild_item[0]
        self.rightChild = BBTreeNode(rightChild_item, self.capacity, self.value)


class BBTree(object):
    def __init__(self, items, capacity):
        self.node = BBTreeNode(items, capacity, 0)

def createItem():
    i = 0
    for w, v in zip(info[0], info[1]):
        items.append(Item(i, v, w))
        i += 1

if __name__ == "__main__":
    # 设定bag容量
    cap = 10
    # 设定物品数量、价值、重量
    item_num = 4
    info = [[10, 5, 3, 1.9],
            [2, 3, 5, 10]]
    items = []
    createItem()
    # 设定放置顺序/策略
    order = [1, 2, 3, 4]
    # 设定节点选择策略
    # 开始放置

    # 计算上界下界
    pass