def split_and_join(line):
    # write your code here
    string,b='',0
    for f in range(len(line)):
        if line[f] == ' ':
            string+=line[b:f]+'-'
            b=f+1
    string+=line[b:]
    return string

if __name__ == '__main__':
    line = input()
    result = split_and_join('this is a string')
    print(result)