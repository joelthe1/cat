import numpy as np

def subset_sum(n, W):
    M = np.empty([n, W], dtype=int)
    for x in range(W):
        M[0][x] = 0
    for x in range(n):
        M[x][0] = 0
    for i in range(1,n):
        for w in range(1,W):
            wi = len(words[i-1])
            if W < wi or w - wi < 0:
                M[i][w] = M[i-1][w]
            else:
                M[i][w] = max(M[i-1][w], wi + M[i-1][w-wi])
    return M

def find_sol(i, w):
    wi = len(words[i-1])
    if i <= 0:
        return
    if w - wi < 0:
        wfile.write(words[i-1] + ', ')
        find_sol(i-1, w)
    elif M[i][w] == M[i-1][w] and M[i][w] == (wi + M[i-1][w-wi]):
        find_sol(i-1, w)
    elif M[i][w] == (wi + M[i-1][w-wi]):
        wfile.write(words[i-1] + ', ')
        find_sol(i-1, w-wi)

words = ['yo', 'no', 'him']
nval = 3 + 1
Wval = 6 + 1
M = subset_sum(nval, Wval)
#print M
print 'Done processing. The max value is', M[nval-1][Wval-1]
if M[nval-1][Wval-1] <= 0:
    print 'No solution found.'
    exit()

wfile = open('output.txt', 'w')
find_sol(nval-1, Wval-1)
wfile.close()
