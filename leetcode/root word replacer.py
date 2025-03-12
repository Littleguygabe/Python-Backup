def replaceWords(dictionary,sentence):
    final = []
    worddict = {}
    sentence = sentence.split(' ')
    for word in sentence:
        worddict[word] = None
    for word in sentence:
        rooted = False
        for root in dictionary:
            if root in word:
                if worddict[word] == None:
                    worddict[word] = (root,len(root))
                elif worddict[word][1]==len(root):
                    worddict[word] = (root,len(root))
    return worddict

print(replaceWords(["a","b","c"],"aadsfasf absbs bbab cadsfafs"))


""" def replaceWords(dictionary,sentence):
    final = []
    worddict = {}
    sentence = sentence.split(' ')
    for word in sentence:
        rooted = False
        for root in dictionary:
            if root in word:
                rooted = True
                base = root
        if rooted:
            final.append(base)
        else:
            final.append(word)

    return ' '.join(final) """