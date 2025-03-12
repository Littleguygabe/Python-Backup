array1 = [1,2,3,4,5]
array2 = []

with open('readme.txt', 'r') as f:
    results = f.read()
    f.close()
    for i in range(0,len(results)):
        array2.append(results[i])

    print(results)
    f.close()

    for i in range(len(array2)-1,0,-1):
        print(len(array2))
        if array2[i] == '\n':
            array2.pop(i)

    print(array2)

with open('readme.txt', 'w') as f:
    f.write('')
    f.close()

with open('readme.txt', 'a') as f:
    for i in range(0,len(array1)):
        f.write(str(array1[i])+'\n')
        
    f.close() 