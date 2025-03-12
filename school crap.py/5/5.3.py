import random
one = 0
two = 0
three = 0
four = 0
five = 0
six = 0

for i in range(0,30):
    roll = random.randint(1,6)
    if roll == 1:
        one = one+1
        
    elif roll == 2:
        two = two+1
        
    elif roll == 3:
        three = three+1
        
    elif roll == 4:
        four = four+1
        
    elif roll == 5:
        five = five+1
        
    elif roll == 6:
        six = six + 1
        
print('1 = ',one)
print('2 = ',two)
print('3 = ',three)
print('4 = ',four)
print('5 = ',five)
print('6 = ',six)