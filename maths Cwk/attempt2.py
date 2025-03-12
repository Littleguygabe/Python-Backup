from sympy import *

#A = Matrix([[0, 1, 2, 0, 1], [0, 2, 4, 1, 1], [0, 0, 5, 1, 1]])
A = Matrix ([[0 , 1] ,
            [2 , 1]])

def rref_ops(A):
    rows, cols = A.shape
    operations = []
    
    pivot_col = 0
    for r in range(rows):
        if pivot_col >= cols:
            break
        
        max_row = max(range(r, rows), key=lambda i: abs(A[i, pivot_col]))
        
        if A[max_row, pivot_col] == 0:
            pivot_col += 1
            continue
        
        if max_row != r:
            A = A.elementary_row_op("n<->m", row1=r, row2=max_row)
            operations.append(("swap", r, max_row))
        
        pivot_value = A[r, pivot_col]
        if pivot_value != 1:
            A = A.elementary_row_op("n->kn", row=r, k=1 / pivot_value)
            operations.append(("scale", r, 1 / pivot_value))
        
        for i in range(rows):
            if i != r and A[i, pivot_col] != 0:
                factor = A[i, pivot_col]
                A = A.elementary_row_op("n->n+km", row=i, row2=r, k=-factor)
                operations.append(("replace", i, -factor, r))
    
        pivot_col += 1
    
    # Ensuring proper order of pivots
    curRow = 0
    for i in range(cols):
        for j in range(curRow, rows):
            if A[j, i] == 1:
                A = A.elementary_row_op('n<->m', row1=j, row2=curRow)
                operations.append(('swap', j, curRow))
                curRow += 1
                break

    for i in range(A.rows):
        print(A.row(i))
    return operations

print(rref_ops(A))
