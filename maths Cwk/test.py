from sympy import Matrix

A = Matrix([
    [1,2,3,4],
    [8,9,10,11],
    [0,0,0,0]
    ])


rows,cols = A.shape
curRow = 2

if not all(A.row(curRow)):
    print('zeros')