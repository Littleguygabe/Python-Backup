from sympy import *

def rref_ops(A) -> list :
    rows,cols = A.shape
    operations = []
    pivCount = 0

    for j in range(cols):
        isPiv = False
        for i in range(pivCount,rows):
            if A[i,j]!=0 and not isPiv:
                if pivCount != i:
                    A = A.elementary_row_op('n<->m',row=pivCount,row2=i)
                    operations.append(('swap',pivCount,i))

                    
                if A[pivCount,j]!=1:
                    scale = Rational(1,A[pivCount,j])
                    A = A.elementary_row_op('n->kn',row=pivCount,k=scale)
                    operations.append(('scale',pivCount,scale))

                isPiv=True
                pivCount+=1

                for l in range(rows):
                    if l != pivCount -1 and A[l,j]!=0:
                        replace = Rational(-A[l,j]) if -A[l,j] % 1 !=0 else int(-A[l,j])

                        A = A.elementary_row_op('n->n+km',row=l,row2=pivCount-1,k=replace)
                        operations.append(('replace',l,replace,pivCount-1))


    return operations

A = Matrix([
    [0,1,-2,2,0,-1],
    [0,-2,4,-3,1,5],
    [0,1,-2,3,1,2],

])


print(rref_ops(A))