

matrix = [[1,2,3,4,5],
          [6,7,8,9,10],
          [11,12,13,14,15],
          [16,17,18,19,20],
          [21,22,23,24,25]]


def calculateDeterminant(Matrix):
    if len(matrix[0])!=len(matrix):
        print('Matrix not square')
        return
    
    rows = len(matrix)
    cols = len(matrix[0])

    if rows == 0 or cols == 0:
        print('no matrix')
        return 0

    det = 0

    count = 0

    for curCol in range(cols):
        curVal = matrix[0][curCol]

        matrixMinor = matrix[1:]
        for i in range(len(matrixMinor)):
            matrixMinor[i].pop(curCol)

        val = curVal*calculateDeterminant(matrixMinor) 

        if count//2 == 2:
            det+=val

        else:
            det-=val

        count+=1

        print('running')

    print(det)

calculateDeterminant(matrix)