word = input('Enter a word: ')
vowels = ['a','e','i','o','u']

bp = len(word)-1
new = ''
for letter in word:
    if letter in vowels:
        while word[bp] not in vowels:
            bp-=1
        new+=word[bp]
        bp-=1
    else:
        new+=letter
print(new)