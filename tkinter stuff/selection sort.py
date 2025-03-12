randarray = []
for i in range(50,0,-1):
    randarray.append(i)

print(randarray)

def selectionSort():
    for base in range(0,len(randarray)-1):
        #minimum algorithm
        minimum = len(randarray)
        minimumIndex = 0
        for i in range(base,len(randarray)):
            if randarray[i]<minimum:
                minimum = randarray[i]
                minimumIndex = i

        temp1 = randarray[base]
        randarray[minimumIndex] = temp1

        randarray[base] = minimum

        drawlines(randarray)

selectionSort()