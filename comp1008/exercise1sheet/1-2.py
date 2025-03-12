import numpy as np

#indexing and data slicing
# indexing in numpy works the same way as indexing a normal python array

# array slicing is the same as normal python aswell

arr1 = np.arange(10)
print(arr1)

arr2 = arr1[(arr1>2)&(arr1<8)] #allows for conditional slicing, so this slices all elements that are greater than 2 and less than 8
# can put any condition within the slice