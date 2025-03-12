s = 'IIM'

vals = {}
vals['I'] = 1
vals['V'] = 5
vals['X'] = 10
vals['L'] = 50
vals['C'] = 100
vals['D'] = 500
vals['M'] = 1000

total = 0

for i in range(len(s)):
    if i <len(s)-2 and vals[s[i]]<vals[s[i+1]]:
        total -= vals[s[i]]
    else:
        total += vals[s[i]]
    
print(total)