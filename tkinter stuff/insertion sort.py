numarr =[]
for i in range(5,0,-1):
    numarr.append(i)

def insertionSort(arr):
     
    if (n := len(arr)) <= 1:
      return
    for i in range(1, n):
         
        key = arr[i]
 
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >=0 and key < arr[j] :
                arr[j+1] = arr[j]
                j -= 1
                
        arr[j+1] = key
        print(arr)
        
insertionSort(numarr)
print(numarr)