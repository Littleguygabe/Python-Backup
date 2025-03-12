string = input('enter string:')
varr = ['a','e','i','o','u']
flipvowels = []
for letter in string:
    if letter in varr:
        flipvowels.append(letter)
newString = ''
for letter in string:
    if letter in varr:
        newString+=flipvowels.pop()
    else:
        newString+=letter
print(newString)
