def fracaddsub(expression):
    stack = []

    symbols = {
        '+':(lambda a,b:a+b),
        '-':(lambda a,b:a-b),
        '/':(lambda a,b:a/b),
    }   

    i = 0
    while i!=len(expression):
        if expression[i]!='/':
            stack.append(expression[i])
            i+=1
        else:
            numerator = stack.pop()
            stack.append(int(numerator)/int(expression[i+1]))
            i+=2

    print(stack)

    total = 0
    i = 0
    while i!=len(stack):
        print(stack[i])
        if stack[i] in symbols:
            print(f'called dict {total},{stack[i]},{stack[i+1]}')
            symbols[stack[i]](total,stack[i+1])
            print(total)

            i+=1
        else:
            i+=1
    print('total:')
    print(total)
        
    print('a third:')
    print(f'{(total).as_integer_ratio()[0]}/{(total).as_integer_ratio()[1]}')


    # translate stack

fracaddsub("-1/2+1/2+1/3")