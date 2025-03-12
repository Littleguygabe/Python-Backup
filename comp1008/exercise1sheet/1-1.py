import numpy as np

testArr = np.zeros((3,3))
print(testArr)

print(testArr.dtype) #dtype -> just lists the data type of the array
print(testArr.shape) #the shape of the numpy array
print(testArr.size) #the number of elements in the numpy array


rangeArr = np.arange(0,20) #creates an array from the first arg (inclusive) to the last arg (exclusive) with a step specified by the 3rd arg (default = 1)
                           #similar syntax to a for loop is (start,end,step)
x,y,z = 0,1,5

linspaceArr = np.linspace(x,y,z) #creates an array of z elements evenly spaced between x and y

x,y=3,3
randomArr = np.random.random((x,y)) #creates a x*y array of uniformly distributed values between [0,1)
