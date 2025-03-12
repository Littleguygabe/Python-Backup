compressed_arr = []

def compression(string):
    index = 0
    compressed_arr = []
    print('func')
    print(len(string))
    while index != len(string):
        cont_value = 0
        current_letter = string[index]
        compressed_arr.append(current_letter)
        unbroken = True

        while unbroken == True:
            for i in range(index,len(string)-index):
                if string[index] == string[i]:
                    cont_value+=1

                else:
                    unbroken=False
        compressed_arr.append(cont_value)
        index+=cont_value
        print(index)
        print(compressed_arr)

word = str(input(':'))
compression(word)