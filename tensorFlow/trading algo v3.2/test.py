import time
import os 

loadingSymbols = ['▂','▃','▅','▇','▅','▃']
i = 0
while True:
    start = (i%len(loadingSymbols))
    for j in range(len(loadingSymbols)):
        index = (start+j)%len(loadingSymbols)
        print(loadingSymbols[index],end='')

    print()
    time.sleep(0.1)
    i+=1
    os.system('cls')