string = input('enter a string to be compressed:')
front = 0
back = 0
arr = []
while front<len(string):
    try:
        while string[back] == string[front]:
            front+=1
    except:
        pass
    arr.append(string[back])
    arr.append(front-back)
    arr.append(' ')

    back = front
for letter in arr:
    print(letter,end = '')