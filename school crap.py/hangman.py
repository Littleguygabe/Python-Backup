import random
complete = False
wordArr = []
displayArr = []
word = input('what is the word to be guessed')

cons = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
vowels = ['a','e','i','o','u']
for i in range(0,len(word)):
    wordArr.append(word[i])
    displayArr.append('_')

print(f'the Word Array is: {wordArr}')
print(f'The Show Array is: {displayArr}')
print('')
print(f'Remaining Consonants are: {cons}')
print(f'Remaining Vowels are: {vowels}')
print('')

while not complete:
    while len(vowels)>0:
        vowel_guess = random.randint(0,len(vowels)-1)
        """ print(f'Positiion is: {vowel_guess}')
        print(f'Letter is: {vowels[vowel_guess]}') """
        vowel_letter = vowels.pop(vowel_guess)
        for i in range(0,len(word)):
            if vowel_letter==word[i]:
                print('')
                print(f'Letter Guessed Correctly: {vowel_letter}')
                displayArr[i] = vowel_letter
                print(displayArr)

    while len(cons)>0:
        con_guess = random.randint(0,len(cons)-1)
        con_letter = cons.pop(con_guess)
        for i in range(0,len(word)):
            if con_letter==word[i]:
                print('')
                print(f'Letter Guessed Correctly: {vowel_letter}')
                displayArr[i] = con_letter
                print(displayArr)