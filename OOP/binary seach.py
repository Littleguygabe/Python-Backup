def search(arr,target):
    n = len(arr)
    if arr[n//2] == target:
        return n//2

    elif arr[n//2]<target:
        search(arr[(n//2)+1:],target)
    
    else:
        search(arr[:(n//2)],target)
        


array = [1,2,3,4,5,6,7,8,9]
print(search(array,2)) 