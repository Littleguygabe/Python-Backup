def frequencysort(s):
    letterDict = {}
    for letter in s:
        if letter not in letterDict:
            letterDict[letter]=1
        else:
            letterDict[letter]+=1
   

s = 'tree'
print(frequencysort(s))