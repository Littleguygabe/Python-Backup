def reverse(x): 
    if x<0:
        x*=-1
        return int(''.join(reversed(list(str(x)))))*-1
    return int(''.join(reversed(list(str(x)))))
    

print(reverse(-123))