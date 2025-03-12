n1 = int(input('Enter Num 1:'))
n2= int(input('Enter Num 2:'))
def amicable(n1,n2):
    factors = []
    for i in range(1,n1):
        if n1%i == 0:
            factors.append(i)
            
    if sum(factors) == n2:
        return True

if amicable(n1,n2) and amicable(n2,n1):
    print('Numbers are amicable')

