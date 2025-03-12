def zec(n):
    zecs = []
    while n>0:
        fmax = fib_max(n)
        n-=fmax
        zecs.append(fmax)
    return zecs

def fib_max(n):
    a,b = 1,2
    while a+b<=n:
        a,b = iterate_fib(a,b)
    
    return b
        
def iterate_fib(a,b):
    return b, a+b

print(zec(21))