arr = [1,7]
k = 1

count = 0
fracs = {}
while count<len(arr):
    for num in arr:
        frac = arr[count]/num
        val = (arr[count],num)
        if frac not in fracs and frac<1:
            fracs[frac] = val
    count+=1

print((list(fracs[sorted(fracs)[k-1]])))