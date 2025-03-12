n = '1222311'
counter=0

i=0
base=n[i]
arr=[]
while i<len(n):
    if n[i] == base:
        counter+=1
    else:
        arr.append((base,counter))
        base=n[i]
        counter=1
    i+=1
arr.append((base,counter))
print(arr)