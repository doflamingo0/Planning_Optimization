import time
from ortools.sat.python import cp_model
import numpy as np
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
N,M,Q,d,q = input('test_30_14.txt')
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

x = {}
for i in range(M+2):
    for j in range(M+2):
        if i != j:
            x[i, j] = model.NewIntVar(0, 1, 'x['+str(i) +', '+str(j)+']')

# neu ke i duoc i duoc den thi y[i] =1 va nguoc lai
y = [model.NewIntVar(0,1,'y['+str(i)+']') for i in range(0,M+2)]
# tong quang duong tu 0 den diem i
z = [model.NewIntVar(0,maxd,'z['+str(i)+']') for i in range(0,M+2)]

#constraint
#khoi tao gia bien
model.Add(y[0]==1)
model.Add(y[M+1]==1)
model.Add(z[0]==0)
model.Add(sum(x[0,i] for i in range(1,M+1))==1)
model.Add(sum(x[i,M+1] for i in range(1,M+1))==1)

#constraint 2

for i in range(M+1):
    for j in range(1,M+2):
    	if i !=j:
	        # x[i] = j => y[i] +y[j] =2
	        b= model.NewBoolVar('b')
	        model.Add(x[i,j]==1).OnlyEnforceIf(b)
	        model.Add(x[i,j]!=1).OnlyEnforceIf(b.Not())
	        model.Add(y[i]+y[j]==2).OnlyEnforceIf(b)
#constraint 3
for i in range(1,M+1):
	b= model.NewBoolVar('b')
	model.Add(y[i]==1).OnlyEnforceIf(b)
	model.Add(y[i]!=1).OnlyEnforceIf(b.Not())
	model.Add(sum(x[i,j] for j in range(1,M+2) if i!=j)==1).OnlyEnforceIf(b)

			


#constraint 4
for i in range(1,M+1):
	b= model.NewBoolVar('b')
	model.Add(y[i]==1).OnlyEnforceIf(b)
	model.Add(y[i]!=1).OnlyEnforceIf(b.Not())
	model.Add(sum(x[j,i] for j in range(M+1) if i!=j)==1).OnlyEnforceIf(b)


#constraint 5
for i in range(M+1):
    for j in range(1,M+2):
    	if i!=j:
	        b= model.NewBoolVar('b')
	        model.Add(x[i,j]==1).OnlyEnforceIf(b)
	        model.Add(x[i,j]!=1).OnlyEnforceIf(b.Not())
	        model.Add(z[i]+d[i%(M+1)][j%(M+1)]==z[j]).OnlyEnforceIf(b)

#constraint 5
for i in range(N):
    model.Add(sum(Q[i][j]*y[j] for j in range(M+1)) >= q[i])
for i in range(N):
    model.Add(sum(Q[i][j]*y[j] for j in range(M+1)) <= total[i])

#objective
f = model.NewIntVar(0,maxd,'f')
model.Add(f>=sum(x[i,j]*d[i%(M+1)][j%(M+1)] for i in range(M+2) for j in range(M+2) if i!=j))


#khoi tao solver
model.Minimize(f)
solver = cp_model.CpSolver()
status = solver.Solve(model)

rs = np.array([[0 for i in range(M+2)] for j in range(M+2)])

if status == cp_model.OPTIMAL:
    print('Obj = %i' % solver.ObjectiveValue())

    for i in range(M+2):
    	for j in range(M+2):
    		if i!=j:
        		rs[i][j] = solver.Value(x[i,j])
# tim kiem lai duong di toi uu
def trace(M, rs):
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


print('trace: ',trace(M,rs))
t = time.time() - t1
print('time: %.2f'%t)
