def isValid(s):
    stack = []
    openers = ['(','[','{']

    ocLink = {')':'(',']':'[','}':'{'}

    for item in s:
        if item in openers:
            stack.append(item)
        else:
            try:
                if stack.pop()!=ocLink[item]:
                    return False
            except:
                return False
    if len(stack)!=0:
        return False

    return True

string = '([)]'
print(isValid(string))