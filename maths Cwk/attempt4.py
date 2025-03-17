from sympy import Matrix

def printMatrix(A):
    rows, cols = A.shape

    for i in range(rows):
        for j in range(cols):
            print('\t',A[i,j],end = ' ')

        print()

    print()
   
def rref_ops(A):
    pass



A = Matrix([
    [0,1,-2,2,0,-1],
    [0,-2,4,-3,1,5],
    [0,1,-2,3,1,2],

])


print(rref_ops(A))

