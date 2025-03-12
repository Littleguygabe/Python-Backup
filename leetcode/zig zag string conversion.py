def convert(s,numRows):
    if numRows== 1:
        return s

    arr = ['']*numRows
    dir = 1
    aind = 0
    for i in s:
        arr[aind]+=i

        if aind == 0:
            dir = 1
        elif aind == numRows-1:
            dir = -1
        
        aind+=dir
    return ''.join(arr)


print(convert('ab',1))