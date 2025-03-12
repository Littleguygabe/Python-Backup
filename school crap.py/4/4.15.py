from datetime import datetime,timedelta

str_d1 = input('enter birth day date (YYYY/MM/DD) ')
d1 = datetime.strptime(str_d1, "%Y/%m/%d")
d2 = d1 + timedelta(days=1)
print(d2.strftime('%Y/%m/%d'))