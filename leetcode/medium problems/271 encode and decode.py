def encode(strs):
    string = ''
    for item in strs:
        string += item + '|'

    return string

def decode(s):
    newlist = []
    string = ''
    for item in s:
        if item !='|':
            string+=item
        else:
            newlist.append(string)
            string = ''
    return newlist

list1 = ["neet","code","love","you"]


print(encode(list1))
print(decode(encode(list1)))