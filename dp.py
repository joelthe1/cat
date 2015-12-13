import numpy as np

def subset_sum(n, W):
    M = np.empty([n, W], dtype=int)
#    print M, words
    for x in range(W):
        M[0][x] = 0
    for x in range(n):
        M[x][0] = 0
    for i in range(1,n):
        for w in range(1,W):
#            vi = compute_value(i, M)
            wi = len(words[i-1])
            if W < wi or w - wi < 0:
                M[i][w] = M[i-1][w]
            else:
                M[i][w] = max(M[i-1][w], wi + M[i-1][w-wi])
    print M
    return M[n-1][W-1]

words = ['him', 'yo', 'no']
nval = 3 + 1
Wval = 6 + 1
print subset_sum(nval, Wval)
