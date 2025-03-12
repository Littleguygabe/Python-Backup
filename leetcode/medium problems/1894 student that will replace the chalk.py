def solution(chalk,k):
    i = 0

    k = k%sum(chalk)

    while True:
        k-=chalk[i%len(chalk)]

        if k<0:
            return i%(len(chalk))
        i+=1

chalk = [3,4,1,2]
k = 25
print(solution(chalk,k))