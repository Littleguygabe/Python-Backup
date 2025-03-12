import random
upper = int(input('enter upper '))
lower = int(input('enter lower '))
count = 0
finished = False

def higherOrLower():
    global lower, upper, count
    global finished
    guess = random.randint(lower,upper)
    check = input(f'is your number equal to or higher or lower than {guess} (E/H/L) ')
    check = check.upper()

    if check == 'H':
        lower = guess
        count += 1

    elif check == 'L':
        upper = guess
        count += 1

    elif check == 'E':
        print(f'your number was {guess}')
        print(f'and it took {count} attempt(s)')
        finished = True

while True:
    higherOrLower()
    if finished == True:
        break