T = []
O = []
E = []
for i in range(1,101):
    if i%2 == 0:
        E.append(i)
        
    else:
        O.append(i)
        
    for k in range(i):
        T.append(i)
        
print(E)
print(O)

def combineLists(R,L):
    return 