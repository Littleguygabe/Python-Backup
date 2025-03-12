def primefactors(num):
    i = 2
    while True:

        if i>num:
            break

        if num%i == 0:
            print(num,end=' ')
            i+=1


num = 20
primefactors(num)