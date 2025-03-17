from sympy import Matrix

def printMatrix(A):
    rows, cols = A.shape

    for i in range(rows):
        for j in range(cols):
            print('\t',A[i,j],end = ' ')

        print()

    print()

   

def rref_ops(A):
    A = A.copy()  
    rows, cols = A.shape

    printMatrix(A)


    lead = 0
    operations = []  
    for r in range(rows):
        if lead >= cols:  
            break

        # want to check if any rows are dependent


        i = r
        while i < rows and A[i, lead] == 0:
            i += 1 #iterates down a column specified by lead

        if i == rows:  
            lead += 1 #if i is the same as the number of rows there is no pivot
                      #so moves to the next column
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
    curRow = 0
    while curRow!=rows:


        for j in range(curRow+1,rows):
            divisible = all((b/a).is_Integer for a,b in zip(A.row(curRow),A.row(j)) if a!=0)
            if divisible:
                c = -(A[j,-1]/A[curRow,-1])
                A = A.elementary_row_op('n->n+km',row=j,row2=curRow,k=c)
                print('appending op')
                operations.append(('scale',j,c))
        curRow+=1

    printMatrix(A)

    return operations


A = Matrix([
    [0,1,-2,2,0,-1],
    [0,-2,4,-3,1,5],
    [0,1,-2,3,1,2],

])


print(rref_ops(A))
