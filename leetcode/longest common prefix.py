def lcp(strs):
    string = ''
    front = sorted(strs)[0]
    back = sorted(strs)[-1]
    
    for i in range(min(len(front),len(back))):
        if front[i] != back[i]:
            return string
            
        string += front[i]
        
    return string

strs = ["flower","flow"]
print(lcp(strs))