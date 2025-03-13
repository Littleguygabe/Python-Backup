from sympy import Matrix

def rref_ops(A):
    A = A.copy()  
    rows, cols = A.shape
    lead = 0
    operations = []  
    for r in range(rows):
        if lead >= cols:  
            break


        i = r
        while i < rows and A[i, lead] == 0:
            i += 1

        if i == rows:  
            lead += 1
            continue


        if i != r:
            A.row_swap(i, r)
            operations.append(('swap',r,i))

        pivot = A[r, lead]
        if pivot != 1:
            for j in range(cols):
                A[r, j] /= pivot
            operations.append(('scale',r,1/pivot))

        for i in range(rows):
            if i != r:
                factor = A[i, lead]
                if factor != 0:
                    for j in range(cols):
                        A[i, j] -= factor * A[r, j]
                    operations.append(('replace',i,-1*factor,r))
        lead += 1  

        ## need to check that the rows are in the correct order and that an linearly dependent rows are removed


    for i in range(rows):
        for j in range(cols):
            print('\t',A[i,j],end = ' ')

        print()

    return operations


A = Matrix([
    [0,1,-2,2,0,-1],
    [0,-2,4,-3,1,5],
    [0,1,-2,3,1,2],

])


print(rref_ops(A))

