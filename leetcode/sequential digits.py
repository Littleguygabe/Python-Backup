import time
start = time.time()
low = 10
high = 1000000000

print('running')

list=[]
while low<=high:
    count = 1
    for k in range(len(str(low))-1):
        if int(str(low)[k]) == int(str(low)[k+1])-1:
            count+=1

    if count == len(str(low)):
        list.append(low)
        roundedLen = len(str(round(low,((len(str(low))-1)*-1))))
        low+=(10**roundedLen)
        
        

    low+=1

print(list)
print(time.time()-start,'s')