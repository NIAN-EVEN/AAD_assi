import numpy as np
from pulp import *

class Assignment(object):
    def __init__(self, task_num, mechine_num):
        self.task = task_num
        self.mechine = mechine_num

def GL_LP(assignment, time_using):
    X = []
    machine_num = assignment.shape[0]
    task_num = assignment.shape[1]
    prob = LpProblem('load balacing', LpMinimize)
    for i in range(machine_num):
        machine = []
        for j in range(task_num):
            var = 'x' + str(i) + str(j)
            machine.append(LpVariable(var, lowBound = 0))
        X.append(machine)
    # formulate target function
    L = LpVariable('L', lowBound=0, upBound=2*sum(time_using)/machine_num)
    # add target function
    prob += L

    # calculate constrains on machine
    machine_constrains = []
    for i in range(machine_num):
        con = 0
        for j in range(task_num):
            con += assignment[i][j]*X[i][j]
        machine_constrains.append(con<=L)

    # calculate constrains on task
    task_constrains = []
    for j in range(task_num):
        con = 0
        for i in range(machine_num):
            con += assignment[i][j]*X[i][j]
        task_constrains.append(con == time_using[j])

    #add machine constrains
    for i in range(machine_num):
        prob += machine_constrains[i]

    # add task constrains
    for j in range(task_num):
        prob += task_constrains[j]

    status = prob.solve()

    print(status)
    print(LpStatus[status])
    print(value(prob.objective))

    for var in prob.variables():
        print(var.name + "=" + str(var.varValue))
    pass


if __name__ == '__main__':
    # assi = np.array([[1, 1, 0, 0],
    #                  [0, 1, 1, 0],
    #                  [0, 0, 1, 1]])
    assi = np.array([[1, 1, 0, 0, 0, 0],
                     [0, 1, 1, 0, 1, 0],
                     [0, 0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 1, 1]])
    time_using = np.array([3, 6, 6, 4, 3, 6])
    GL_LP(assi, time_using)
    pass