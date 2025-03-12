montharray = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
while True:
    month = int(input('enter a month '))
    if month<13 and month>0:
        month = month - 1
        print(montharray[month])
        break
        
    else:
        print('must be between 1 - 12')
