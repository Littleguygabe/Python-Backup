def valid(string):
    if len(string)<5 or len(string)>7:
        print('length')
        return False
    total = 0
    dict = {}
    for letter in string:
        total+=ord(letter)
        if ord(letter)>90 or ord(letter)<65:
            print('Not uppper')
            return False
        
        if letter not in dict:
            dict[letter] = 1
        else:
            print('dupes')
            return False
    if total<420 or total>600:
        print('score')
        print(total)
        return False
    
while not valid(string = input('enter string: ')):
    print('Invalid string')