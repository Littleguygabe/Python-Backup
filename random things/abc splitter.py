import time
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alen = len(alphabet)

def abc(n,total):
    sections = [0]*n
    for i in range(total):
        sections[i%n]+=1


    return sections

start = time.time()
print(abc(12,26))
print(f'finished in {time.time()-start}s')