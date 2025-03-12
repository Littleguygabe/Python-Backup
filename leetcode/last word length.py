s = "a"

def func(s):
    back = len(s)
    for i in range(len(s)-2,0,-1):
        if s[i+1] == ' ':
            back = i+1
        if s[i]==' ' and s[i+1]!=' ':
            return int(len(s[i+1:back]))
    
    return len(s)
        
print(func(s))