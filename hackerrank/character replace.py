def mutate_string(string, position, character):
    word = ''
    word+=(string[:position])
    word+=(character)
    word+=(string[position+1:])
    return(word)

if __name__ == '__main__':
    s = 'abracadabra'
    i, c = 5,'k'
    s_new = mutate_string(s, int(i), c)
    print(s_new)