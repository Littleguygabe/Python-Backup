def solution(temperatures):
    # stack solution allows for linear time complexity
    
    res = [0] * len(temperatures)
    stack = [] # store value and index [val,index]

    for i,t in enumerate(temperatures):
        while stack and t>stack[-1][0]:
            temp,tInd = stack.pop()
            res[tInd] = (i-tInd)

        stack.append([t,i])

    return res


temperatures = [73,74,75,71,69,72,76,73]
print(solution(temperatures))