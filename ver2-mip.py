import time
from ortools.linear_solver import pywraplp
import numpy as np

# Read data
def input(fileName):
    with open(fileName, 'r') as f:
        [N, M] = [int(x) for x in f.readline().split()]
        
        # them cot 0 vao cot Q[i][0]
        Q = []
        for i in range(N):
            tmp =[int(x) for x in f.readline().split()]
            tmp.append(int(0))
            tmp = tmp[-1:] + tmp[:-1]
            Q.append(tmp)

        d = []
        for i in range(M+1):
            d.append([int(x) for x in f.readline().split()])
        
        q = [int(x) for x in f.readline().split()]
        
        return N, M, Q, d, q

C = 1000

def CreateSolverAndVariables(M, maxd):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    x = {}
    for i in range(M+2):
        for j in range(M+2):
            if i != j:
                x[i, j] = solver.IntVar(0, 1, 'x('+str(i) +', '+str(j)+')')

    y = [solver.IntVar(0, 1, 'y('+str(i)+')') for i in range(M+2)]
    z = [solver.IntVar(0, maxd, 'z('+str(i)+')') for i in range(M+2)] # 0' === M+1
    return x, y, z, solver

# Constraint 1: Default Constraints
def CreateConstraint1(solver, M, x, y, z):
    # y[0] = 1
    c = solver.Constraint(1,1)
    c.SetCoefficient(y[0],1)

    # y[M+1] = 1
    c = solver.Constraint(1,1)
    c.SetCoefficient(y[M+1],1)

    # tai diem M+1, luon co 1 luong di vao
    c = solver.Constraint(1,1)
    for i in range(1,M+1):
        c.SetCoefficient(x[i, M+1],1)

    # Tai diem 0, luon co 1 luong di ra
    c = solver.Constraint(1,1)
    for i in range(1,M+1):
        c.SetCoefficient(x[0,i],1)
    
    c = solver.Constraint(0,0)
    c.SetCoefficient(z[0],1)

# Constraint 2
# x[i,j] = 1 -> y[i] + y[j] = 2
def CreateConstraint2(solver, M, x, y):
    for i in range(1,M+1):
        for j in range(1,M+1):
            if i != j:
                solver.Add(y[i]+y[j] + C*(1-x[i,j]) >= 2)
                solver.Add(y[i]+y[j] + C*(x[i,j]-1) <= 2)

# Constraint 3 and 4
def CreateConstraint3and4(solver, M, x, y):
    # y[i] = 1 --> sum(x[i,j]) (j=1->M+1) = sum(x[j,i]) (j=0->M) = 1  voi moi i =1..M
    for i in range(1,M+1):
        c = solver.Constraint(1-C, C)
        c.SetCoefficient(y[i], -C)
        for j in range(1,M+2):
            if i != j:
                c.SetCoefficient(x[i,j], 1)
        
        c = solver.Constraint(-C,1+C)
        c.SetCoefficient(y[i], C)
        for j in range(1,M+2):
            if i != j:
                c.SetCoefficient(x[i,j], 1)

        c = solver.Constraint(1-C, C)
        c.SetCoefficient(y[i], -C)
        for j in range(M+1):
            if i != j:
                c.SetCoefficient(x[j,i], 1)
        
        c = solver.Constraint(-C,1+C)
        c.SetCoefficient(y[i], C)
        for j in range(M+1):
            if i != j:
                c.SetCoefficient(x[j,i], 1)

# Constraint 5
# x[i,j] = 1 -> z[j] = z[i] + d[i,j]
def CreateConstraint5(solver,M,x,z,d):
    for i in range(M+2):
        for j in range(M+2):
            if i != j:
                solver.Add(z[j] + C*(1-x[i,j]) >= z[i]+d[i%(M+1)][j%(M+1)])
                solver.Add(z[j] + C*(x[i,j]-1) <= z[i]+ d[i%(M+1)][j%(M+1)])


# Constraint 6: quantity constraints
def CreateConstraint6(solver, M, N, y, q, Q, total):
    for i in range(N):
        c = solver.Constraint(q[i], total[i])
        for j in range(1,M+1):
            c.SetCoefficient(y[j%(M+1)], Q[i][j%(M+1)])


def CreateObjective(solver, M, x, d):
    obj = solver.Objective()
    for i in range(M+2):
        for j in range(M+2):
            if i != j:
                obj.SetCoefficient(x[i,j], d[i%(M+1)][j%(M+1)])
    
    obj.SetMinimization()

def Trace(M, rs):
    tmp = 0
    trace = [0]
    while True:
        for i in range(M+2):
            if i != tmp and rs[tmp,i] > 0:
                tmp = i
                break
        if tmp == M+1:
            break
        trace.append(tmp)
    
    return trace

def ComputeItems(M, N, Q, y):
    rs = [0 for i in range(N)]
    for i in range(N):
        for j in range(M+1):
            if y[j].solution_value() > 0:
                rs[i] = rs[i] + Q[i][j]
    return rs

def PrintSol(M, rs):
    trace = Trace(M, rs)
    print("Route:", trace)


def Solve(M, N, q, Q, d, total, maxd):
    x, y, z, solver = CreateSolverAndVariables(M, maxd)
    CreateConstraint1(solver, M, x, y, z)
    CreateConstraint2(solver, M, x, y)
    CreateConstraint3and4(solver, M, x, y)
    CreateConstraint5(solver, M, x, z, d)
    CreateConstraint6(solver, M, N, y, q, Q, total)
    CreateObjective(solver, M, x, d)

    result_status = solver.Solve()

    # The problem has optimal solution.
    assert result_status == pywraplp.Solver.OPTIMAL
    print('Objective =', solver.Objective().Value())

    rs = np.array([[0 for i in range(M+2)] for j in range(M+2)])
    for i in range(M+2):
        for j in range(M+2):
            if i != j:
                rs[i, j] = x[i,j].solution_value()
    
    # print z[i]
    # for i in range(M+2):
    #     print('z['+str(i)+'] =', z[i].solution_value())

    return rs

def main():
    t1 = time.time()
    N, M, Q, d, q = input('test_100_80.txt')
    total = [0 for i in range(N)]
    for i in range(N):
        for j in range(M+1):
            total[i] = total[i] + Q[i][j]

    maxd = 0
    for i in range(M+1):
        for j in range(i+1,M+1):
            maxd = maxd + d[i][j]
    rs = Solve(M, N, q, Q, d, total, maxd)
    PrintSol(M,rs)

    # print('Order:', q)
    # print('So luong:', ComputeItems(M, N, Q, y))
    t2 = time.time()
    
    print('Time:',round(t2-t1, 2), 'seconds')


if __name__ == '__main__':
    main()