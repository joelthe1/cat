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

#def find_sol(i, w):
#    wi = len(words[i-1])
#    if i <= 0:
#        return
#    if w - wi < 0:
#        wfile.write(words[i-1] + ', ')
#        find_sol(i-1, w)
#    elif M[i][w] == M[i-1][w] and M[i][w] == (wi + M[i-1][w-wi]):
#        find_sol(i-1, w)
#    elif M[i][w] == (wi + M[i-1][w-wi]):
#        wfile.write(words[i-1] + ', ')
#        find_sol(i-1, w-wi)

def build_tree():
    stack = []
    tree = {}
    
    tree['__root'] = []
    for child in find_children((nval+1,Wval+1)):
        stack.append(child)
        tree['__root'].append(words[child[0]-1])
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
    if i <= 1 or (i <= nval and w-len(words[i-1]) <= 0):
        return children
    if i > nval: #For root assume i=nval+1 and w=Wval+1
        word_len = 1
    else:
        word_len = len(words[i-1])
    w -= word_len
    i -= 1
    while M[i][w] == M[i-1][w]:
        wi = len(words[i-1])
        if M[i][w] == (wi + M[i-1][w-wi]):
            temp = (i,w)
            children.append((i,w))
        i -= 1
    children.append((i,w))
    return children

def traverse(n, counter, route):
    if counter == max_val:
#        print route
        wfile.write(','.join(route)+'\n')
    if counter > max_val:
        return
    children = graph[n]
    if children:
        for child in children:
            temp_route = route[:]
            temp_route.append(child)
            traverse(child, counter+len(child), temp_route)

words = ['yo', 'no', 'him', 'tommy', 'so', 'a']
nval = 6
Wval = 6
M = subset_sum(nval+1, Wval+1)
print M
max_val = M[nval][Wval]
print 'Done processing. The max value is', max_val
if max_val <= 0:
    print 'No solution found.'
    exit()

wfile = open('output.txt', 'w')
#print find_children((7,7))
#print build_tree()
graph = build_tree()
print graph
for root in graph['__root']:
    traverse(root,len(root),[root])
wfile.close()
