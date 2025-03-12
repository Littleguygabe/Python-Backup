total = 0
x = 1
num = int(input('___'))
total = total+num

while num!=0:
    total = total+num
    num = int(input('___'))
    x=x+1
    print(total/x)
        
print(num)