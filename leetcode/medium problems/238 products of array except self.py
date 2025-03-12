def solution(nums):
    output = []
    temp = setuptemp(nums)
    for i in range(len(nums)):
        temp.pop(i)
        output.append(arrayProd(temp))
        temp = setuptemp(nums)

    return output

def setuptemp(a):
    temp = []
    for item in a:
        temp.append(item)
    return temp

def arrayProd(a):
    total = 1
    for item in a:
        total *= item 
    return total
print(solution([1,2,4,6]))