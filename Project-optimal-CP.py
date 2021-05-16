import time
from ortools.sat.python import cp_model

#input
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

t1 = time.time()
N,M,Q,d,q = input('test_30_9.txt')
# xu ly du lieu
# maxd la tong tat ca cac canh cua do thi duong di
maxd = 0
for i in range(M+1):
    for j in range(i+1,M+1):
        maxd = maxd + d[i][j]
# total[i] la tong so luong cua moi mat hang i
total = [0 for i in range(N)]
for i in range(N):
    for j in range(M+1):
        total[i] = total[i] + Q[i][j]
#model
# variable
model = cp_model.CpModel()
# diem tiep theo cua hanh trinh tu i
x = [model.NewIntVar(1,M+1,'x['+str(i)+']') for i in range(0,M+1)]
# neu ke i duoc i duoc den thi y[i] =1 va nguoc lai
y = [model.NewIntVar(0,1,'y['+str(i)+']') for i in range(0,M+2)]
# tong quang duong tu 0 den diem i
z = [model.NewIntVar(0,maxd,'z['+str(i)+']') for i in range(0,M+2)]

#constraint
#khoi tao gia bien
model.Add(y[0]==1)
model.Add(y[M+1]==1)
model.Add(z[0]==0)
#constraint 1
for i in range(M+1):
	model.Add(x[i]!=i)
#constraint 2
model.AddAllDifferent(x)
#constraint 3
for i in range(M+1):
    for j in range(1,M+2):
        b= model.NewBoolVar('b')
        model.Add(x[i]==j).OnlyEnforceIf(b)
        model.Add(x[i]!=j).OnlyEnforceIf(b.Not())
        model.Add(y[i]+y[j]==2).OnlyEnforceIf(b)
#constraint 4
for i in range(M+1):
    for j in range(1,M+2):
        b= model.NewBoolVar('b')
        model.Add(x[i]==j).OnlyEnforceIf(b)
        model.Add(x[i]!=j).OnlyEnforceIf(b.Not())
        model.Add(z[i]+d[i%(M+1)][j%(M+1)]==z[j]).OnlyEnforceIf(b)
#constraint 5
for i in range(N):
    model.Add(sum(Q[i][j]*y[j] for j in range(M+1)) >= q[i])
for i in range(N):
    model.Add(sum(Q[i][j]*y[j] for j in range(M+1)) <= total[i])

#khoi tao solver
model.Minimize(z[M+1])
solver = cp_model.CpSolver()
status = solver.Solve(model)

rs = [-1 for i in range(M+1)]

if status == cp_model.OPTIMAL:
    print('Obj = %i' % solver.ObjectiveValue())
    for i in range(M+1):
        rs[i] = solver.Value(x[i])
# tim kiem lai duong di toi uu
def trace(M,rs):
    trace = []
    tmp = 0
    while tmp != M+1:
        trace.append(tmp)
        tmp = rs[tmp]
    return trace

print('trace: ',trace(M,rs))
t = time.time() - t1
print('time: %.2f'%t)


