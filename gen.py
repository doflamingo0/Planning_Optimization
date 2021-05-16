import random as rd

def genData(fileName, N, M):
    with open(fileName, "w") as f:
        f.write(str(N) + " " + str(M) + "\n")

        x = [0 for i in range(N)] # x[i]: total of all items i
        # Generate matrix Q: Q(i,j) is number of item i on table j

        for i in range(N):
            s = ""
            for j in range(M):
                c = rd.randint(1,15)
                x[i] = x[i] + c
                s = s + str(c) + ' '
            s = s + '\n'
            f.write(s)

        # Generate matrix d: d(i,j) is distance between 2 point i and j
        d = [[0 for i in range(M+1)] for j in range(M+1)]
        
        for i in range(M+1):
            for j in range(i, M+1):
                if i != j:
                    d[i][j] = d[j][i] = rd.randint(1, 15)
        
        for i in range(M+1):
            s = ''
            for j in range(M+1):
                s = s + str(d[i][j]) + ' '
            f.write(s + '\n')
        

        # Generate a order include q(i): is number of item i, i = 1...N
        s = ''
        for i in range(N):
            c = rd.randint(1, x[i])
            s = s + str(c) + ' '
        f.write(s)
        f.close()

genData('test_20_10.txt', 20,10)

