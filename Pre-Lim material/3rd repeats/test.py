from itertools import groupby;s=input('Enter a word: ');print(' '.join([k + ' ' + str(len(list(g))) for k, g in groupby(s)]))

