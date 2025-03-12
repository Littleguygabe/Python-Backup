import math
def solution(piles,h):
    l,r = 1,max(piles)

    while l<r:
        k = (l+r)//2
        hours = 0
        for val in piles:
            hours+=math.ceil(val/k)

        if k>=hours:
            l = len(piles)//2

        else:
            r = len(piles)//2

    return k

    

piles = [3,6,7,11]
h = 8
print(solution(piles,h))