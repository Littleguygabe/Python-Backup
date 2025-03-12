num = int(input('_'))

while num%2 != 1:
    num = int(input('_'))

def starPlacer():
    for x in range(num,0,-2):
        offset = (num-x)
        offset = int(offset/2)
        print(' '*offset,'*'*x)

starPlacer()