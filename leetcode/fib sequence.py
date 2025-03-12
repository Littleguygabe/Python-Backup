def fib(n):
    fibN = 1
    prevFibN = 0    
    if n == 1:
        return 0
    
    for i in range(n-1):
        temp = fibN
        fibN+=prevFibN
        prevFibN = temp
    return fibN

for i in range(11):
    print(fib(i))