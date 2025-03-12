def merge_the_tools(string, k):
    # your code goes here
    list = []
    f = 0
    b = 0
    while True:
        f+=1
        if f%k == 0:
            list.append(string[b:f])
            b=f
        if f>=len(string):
            break

    for string in list:
        tempstr = ''
        for character in set(string):
            tempstr+=character
        print(tempstr)
        

if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)