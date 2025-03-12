def solution(word1,word2):
    string = ''
    i=0
    while i < (min(len(word1),len(word2))):
        string+=word1[i]
        string+=word2[i]
        i+=1
    
    if len(word1)>len(word2):
        string+=word1[i:]

    elif len(word2)>len(word1):
        string+=word2[i:]

    return string



word1 = 'ab'
word2 = 'pqrs'

print(solution(word1,word2))