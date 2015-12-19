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

def build_tree():
    stack = []
    tree = {}
    
    tree['root'] = []
    for child in find_children((nval,Wval)):
        stack.append(child)
        tree['root'].append(words[child[0]-1])
    print stack
    while True:
        counter = 0
        while counter <= Wval:
            if len(stack) < 1:
                return tree
            base = stack.pop()
            word = words[base[0]-1]
            if word not in tree:
                tree[word] = []
            for child in find_children(base):
                stack.append(child)
                tree[word].append(words[child[0]-1])
            counter += len(word)

def find_children(base):
    children = []
    i,w = base
    if i <= 1 or w-len(words[i-1]) <= 0:
        return children
    w -= len(words[i-1])
    i -= 1
    while M[i][w] == M[i-1][w]:
        wi = len(words[i-1])
        if M[i][w] == (wi + M[i-1][w-wi]):
            temp = (i,w)
            children.append((i,w))
        i -= 1
    children.append((i,w))
    return children
                                                    
words = ['yo', 'no', 'him', 'tommy', 'so', 'a']
nval = 6
Wval = 6
M = subset_sum(nval+1, Wval+1)
print M
print 'Done processing. The max value is', M[nval][Wval]
if M[nval][Wval] <= 0:
    print 'No solution found.'
    exit()

wfile = open('output.txt', 'w')
find_sol(nval, Wval)
print find_children((5,6))
#print build_tree()
wfile.close()
