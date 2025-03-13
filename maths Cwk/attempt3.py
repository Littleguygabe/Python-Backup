from sympy import Matrix

def rref_ops(A):
    """Compute RREF of A and return the list of operations performed."""
    A = A.copy()  # Work on a copy of the matrix
    rows, cols = A.shape
    lead = 0
    operations = []  # Store elementary row operations

    for r in range(rows):
        if lead >= cols:  # Stop if we exceed the column count
            break

        # Find pivot row
        i = r
        while i < rows and A[i, lead] == 0:
            i += 1

        if i == rows:  # Entire column is zero, move to the next column
            lead += 1
            continue

        # Swap current row with the pivot row if necessary
        if i != r:
            A.row_swap(i, r)
            operations.append(('swap',r,i))
        # Normalize the pivot row (make leading coefficient 1)
        pivot = A[r, lead]
        if pivot != 1:
            for j in range(cols):
                A[r, j] /= pivot
            operations.append(('scale',r,1/pivot))
        # Eliminate all other entries in this column
        for i in range(rows):
            if i != r:
                factor = A[i, lead]
                if factor != 0:
                    for j in range(cols):
                        A[i, j] -= factor * A[r, j]
                    operations.append(('replace',i,-1*factor,r))
        lead += 1  # Move to the next column

    return operations


A = Matrix([
    [0, 1],
    [2, 1]
])

print(rref_ops(A))

