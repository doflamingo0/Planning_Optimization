from os import name
import time

# Read data
def input(fileName):
    with open(fileName, 'r') as f:
        [N, M] = [int(x) for x in f.readline().split()]
        
        Q = []
        for i in range(N):
            Q.append([int(x) for x in f.readline().split()])

        d = []
        for i in range(M+1):
            d.append([int(x) for x in f.readline().split()])
        
        q = [int(x) for x in f.readline().split()]
        
        return N, M, Q, d, q

def check(v):
    return not visited[v]

def checkStop():
    for i in range(N):
        if q[i] != 0:
            return False
    return True

def solution(k):
    global minDistance
    if minDistance > curDistance:
        minDistance = curDistance
        print('update:', minDistance)
        print(x[:k+1])

def TRY(k):
    global q, curDistance
    for v in range(1, M+1):
        if check(v):
            x[k] = v

            # update
            curDistance = curDistance + d[x[k-1]][x[k]]
            visited[v] = True
            r = [0 for i in range(N)]
            for i in range(N):
                r[i] = min(Q[i][v-1], q[i])
                q[i] = q[i] - r[i]
            
            if checkStop():
                solution(k)

            TRY(k+1)

            # Recover
            curDistance = curDistance - d[x[k-1]][x[k]]
            visited[v] = False
            for i in range(N):
                q[i] = q[i] + r[i]


t1 = time.time()
N, M, Q, d, q = input('test_20_10_1.txt')
x = [0 for i in range(M+1)]                 # x[i]: i-th destination
visited = [False for i in range(M+1)]       # visited[i] = True if went to i
curDistance = 0                             
minDistance = 1e9

TRY(1)
t2 = time.time()
print('Time:',round(t2-t1, 2), 'seconds')