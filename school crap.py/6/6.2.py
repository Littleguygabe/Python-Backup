total = 0
def average(numbers):
    global total
    for i in range (0,len(numbers)):
        total = total + numbers[i]
    
    total = total/len(numbers)
    print(total)

numbers = []
num = int(input('_'))
numbers.append(num)
check = input('do you want to enter another number Y/N')
check = check.upper()

while check == 'Y':
    num = int(input('_'))
    numbers.append(num)
    check = input('do you want to enter another number Y/N')
    check = check.upper()

average(numbers)