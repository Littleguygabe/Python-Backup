import numpy as np

arr = np.arange(10)
# can perform a math operation on the variable name and it is automatically applied to every element in the array

print(arr*2) #doubles every element in the array


#also provides statistical operations
print(np.sum(arr)) #sum of the array
print(np.std(arr)) #print the standard deviation of the array
print(np.max(arr)) #max of the array
print(np.min(arr)) #min of the array  

    #^^ pandas also has the same math operations that can be applied to data frames