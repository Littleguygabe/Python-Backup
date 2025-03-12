binary=[]
additional=("0")
num2convert=int(input("input num__  "))

while num2convert>0:
    if (num2convert%2)==0:
        digit=("0")
        num2convert=num2convert/2
    elif(num2convert%2)>0:
        digit=("1")
        num2convert=(num2convert/2)-(0.5)
    binary.append(digit)

while (len(binary))<8:
    binary.append(additional)
    
binary=(list(reversed(binary)))
final="".join(binary)
print(final)
