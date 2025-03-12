from sympy import *
A = Matrix([[0,1,2,0,1],[0,2,4,1,1],[0,0,5,1,1]])

#A.elementary_row_op('n<->m',row1=i,row2=j) # -> swaps rows at index i & j
#A.elementary_row_op("n->n+km",row=i,row2=j,k=c) # -> Ri = Ri + cRj
#A.elementary_row_op("n->kn",row=i,k=c) # -> Ri = cRi

#print(A.rref()) # -> outputs the rref matrix, with a tuple of the pivot columns

def rref(A):
    rows,cols = A.shape
    curPivCol = 0

    for r in range(rows):
        # get with pivot at the top
        if curPivCol>=cols:
            break  

        # while the [row,col] value is 0 move onto the next row
        i = r
        while i<rows and A[i,curPivCol]==0:
            i+=1

        # if i = No Rows then no pivot in column so jump to the next column
        if i == rows:
            curPivCol+=1
            continue 


        A.row_swap(r,i)

        colPivVal = A[r,curPivCol]
        A.row_op(r,lambda x, _: x/colPivVal)

        for j in range(rows):
            if j!=r:
                factorVal = A[j,curPivCol]
                A.row_op(j,lambda x, k:x-factorVal*A[r,k])

        print(A[r,curPivCol])
        if A[r,curPivCol] != 1:
            pivMul = 1/A[r,curPivCol]
            A.row_op(r,lambda x, _:x*pivMul)

        curPivCol+=1

    return A           

print(rref(A))