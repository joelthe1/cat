import numpy as np
import sys
from tqdm import *

def subset_sum(n, W):
    M = np.empty([n, W], dtype=np.ndarray)
    inner = intConvert(permutedString)
    for x in range(W):
        M[0][x] = np.copy(inner)
    for x in range(n):
        M[x][0] = np.copy(inner)
    for i in tqdm(range(1,n),'Calculating Subset-Sum', None, True):
        for w in range(1,W):
            wi = len(words[i-1])
            if W < wi or w - wi < 0:
                M[i][w] = np.copy(M[i-1][w])
                M[i][w][1] = 1 #Set parent route
            else:
                vi = processValue(words[i-1], M[i-1][w-wi])
                if M[i-1][w][0] > vi + M[i-1][w-wi][0] or vi == -100:
                    M[i][w] = np.copy(M[i-1][w])
                    M[i][w][1] = 1 #Set parent route
                elif M[i-1][w][0] < vi + M[i-1][w-wi][0]:
                    tempInner = processInner(words[i-1], M[i-1][w-wi], vi)
                    M[i][w] = tempInner
                    M[i][w][1] = 2 # set parent route
                elif M[i-1][w][0] == vi + M[i-1][w-wi][0]:
                    #No clash handling now
                    M[i][w] = np.copy(M[i-1][w])
                    M[i][w][1] = 1 #Set parent route
    return M

def processClash(inner1, inner2, value):
    countInner1 = 0
    countInner2 = 0
    for x in inner1:
        if x == -1:
            countInner1 += 1
    for x in inner2:
        if x == -1:
            countInner2 += 1
    if countInner1 <= countInner2:
        return np.copy(inner1)
    temp = np.copy(inner2)
    temp[0] += value
    return temp
        

def processInner(word, leftOver, value):
    leftOverCopy = np.copy(leftOver)
    leftOverCopy[0] += value
    for x in word:
        for index, val in enumerate(leftOverCopy[2:]):
            if ord(x) == val:
                leftOverCopy[index+2] = -1
                break
    return leftOverCopy
            

def processValue(word, leftOver):
#    print word, leftOver
    leftOverCopy = np.copy(leftOver)
    wordCounter = 0
    listCounter = 2 #Since [1] has value and [2] has direction. 
    tempWord = sorted(word)
    while listCounter < (Wval+2):
        if wordCounter >= len(tempWord):
            return len(tempWord)
        if ord(tempWord[wordCounter]) == leftOverCopy[listCounter]:
            wordCounter += 1
        listCounter += 1
    return -100

def intConvert(permutedString):
    inner = np.zeros([Wval+2], dtype=int)
    for x,y in enumerate(permutedString):
        inner[x+2] = ord(y)
    inner.sort()
    return inner

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
                if child not in stack:
                    stack.append(child)
                if words[child[0]-1] not in tree[word]:
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

def transpose(n, W, fullM):
    filteredM = np.empty([n, W], dtype=int)
    for i in range(n):
        for w in range(W):
            filteredM[i][w] = fullM[i][w][0]
    return filteredM

def transposeRoute(n, W, fullM):
    filteredM = np.empty([n, W], dtype=int)
    for i in range(n):
        for w in range(W):
            filteredM[i][w] = fullM[i][w][1]
    return filteredM

def traverseRoute(tM):
    i = nval
    w = Wval
    ans = []
    while True:
        if i <= 0 or w <=0:
            print ans
            wfile.write(','.join(ans))
            return
        if tM[i][w] == 2:
            word_len = len(words[i-1])
            ans.append(words[i-1])
            i -= 1
            w -= word_len
        elif tM[i][w] == 1:
            i -= 1

rfile = sys.argv[2]
words = []
nval = 0
with open(rfile) as inputFile:
    permutedString = inputFile.readline().strip()
    for line in inputFile:
        nval += 1
        words.append(line.strip())

Wval = len(permutedString)
#print Wval, nval

fullM = subset_sum(nval+1, Wval+1)
M = transpose(nval+1, Wval+1, fullM)
traversalM = transposeRoute(nval+1, Wval+1, fullM)

print M
max_val = M[nval][Wval]
print 'Done processing. The max value is', max_val
if max_val <= 0:
    print 'No solution found.'
    exit()

wfile = open('output.txt', 'w')
traverseRoute(traversalM)
#graph = build_tree()
#print graph
#for root in tqdm(graph['__root'],'Traversing Graph', None, True):
#    traverse(root,len(root),[root])
wfile.close()
