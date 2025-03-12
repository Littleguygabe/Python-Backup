def solution(matrix,target):

    if len(matrix) == 0:
        return False

    N,M = len(matrix),len(matrix[0])

    i,j = 0, N-1
    while j>=0 and i<M:
        if matrix[j][i] == target:
            return True

        elif matrix[j][i]>target:
            j-=1
        elif matrix[j][i]<target:
            i+=1

    return False

matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]]
target = 31
print(solution(matrix,target))