randarray = []
for i in range(50,0,-1):
    randarray.append(i)
print(f'unsorted:{randarray}')

def cocktailsort():
    start = time.time()
    sorted = False
    while sorted == False:
        for i in range(0,round(len(randarray)/2)):
            changes = 0
            lowerindex = i
            upperindex = len(randarray)-1-i

            templower = randarray[lowerindex]
            if randarray[lowerindex]>randarray[lowerindex+1]:
                randarray[lowerindex] = randarray[lowerindex+1]
                randarray[lowerindex+1] = templower
                changes+=1

            tempupper = randarray[upperindex]
            if randarray[upperindex]<randarray[upperindex-1]:
                randarray[upperindex]=randarray[upperindex-1]
                randarray[upperindex-1]=tempupper
                changes+=1


            if changes == 0:
                sorted = True
    
    timecount = time.time() - start
    print(f'finished in {timecount}s')

cocktailsort()
