
import time

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

def check(v):
    if not visited[v]:
        for i in range(N):
            if q[i] > 0 and Q[i][v] > 0:
                return True
    return False

def checkStop():
    for i in range(N):
        if q[i] != 0:
            return False
    return True

def solution(k):
    global idx
    global minDistance
    if minDistance > curDistance + d[x[k]][0]:
        minDistance = curDistance + d[x[k]][0]
        idx = k+1
        rs[:k+1] = x[:k+1]

def TRY(k):
    global q, curDistance
    for v in range(1, M+1):
        if check(v):
            x[k] = v

            # Update
            curDistance = curDistance + d[x[k-1]][x[k]]
            visited[v] = True
            r = [0 for i in range(N)] # r[i]: la so luong san pham i lay o ban v
            for i in range(N):
                r[i] = min(Q[i][v], q[i])
                q[i] = q[i] - r[i]
            
            if checkStop():
                solution(k)
            if curDistance < minDistance:
                TRY(k+1)

            # Recover
            curDistance = curDistance - d[x[k-1]][x[k]]
            visited[v] = False
            for i in range(N):
                q[i] = q[i] + r[i]


t1 = time.time()
N, M, Q, d, q = input('test_30_15.txt')
x = [0 for i in range(M+1)]                 # x[i]: i-th destination
visited = [False for i in range(M+1)]       # visited[i] = True if went to i
curDistance = 0                             
minDistance = 1e9
rs = [0 for i in range(M+1)]                # result
idx = 0
TRY(1)
print("Objective:", minDistance)
print("Route:", rs[:idx])
t2 = time.time()
print('Time:',t2-t1, 'seconds')