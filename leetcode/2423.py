# can you remove one letter to make all letters the same
word = 'aazz'

def equalFrequency(word):
    dict = {}
    for letter in word:
        if letter in dict:
            dict[letter]+=1
        else:
            dict[letter]=1
    
    base=dict[word[0]]
    total = 0
    for letter in dict:
        print(total)
        total+=abs(base-dict[letter])
    
    if total>1:
        return False

    return True

print(equalFrequency(word))