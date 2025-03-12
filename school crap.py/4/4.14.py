from datetime import datetime

str_d1 = input('enter birth day date (YYYY/MM/DD) ')
str_d2 = input('enter todays date (YYYY/MM/DD) ')

d1 = datetime.strptime(str_d1, "%Y/%m/%d")
d2 = datetime.strptime(str_d2, "%Y/%m/%d")

delta = d2 - d1
print(f'Difference is {delta.days} days')
