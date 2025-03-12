board = [
 ["1","2",".",".","3",".",".",".","."],
 ["4",".",".","5",".",".",".",".","."],
 [".","9","1",".",".",".",".",".","3"],
 ["5",".",".",".","6",".",".",".","4"],
 [".",".",".","8",".","3",".",".","5"],
 ["7",".",".",".","2",".",".",".","6"],
 [".",".",".",".",".",".","2",".","."],
 [".",".",".","4","1","9",".",".","8"],
 [".",".",".",".","8",".",".","7","9"]
 ]

def solution(board):
    #check rows
    for row in board:
        crarr = []
        for item in row:
            if item != '.':
                if item not in crarr:
                    crarr.append(item)
                else:
                    return False
                
    #check columns
    for i in range(len(board[0])):
        ccarr = []
        for row in board:
            if row[i]!='.':
                if row[i] not in ccarr:
                    ccarr.append(row[i])
                else:
                    return False
                
    #check 3x3


    for k in range(0,len(board),3): # top to bottom
        for l in range(0,len(board[i]),3):# left to right

            c3x3arr = []
            for j in range(0,3):
                for i in range(0,3):
                    if board[k+j][l+i] != '.':
                        if board[k+j][l+i] not in c3x3arr:
                            c3x3arr.append(board[k+j][l+i])
                        else:
                            return False
                        
    return True

print(solution(board))