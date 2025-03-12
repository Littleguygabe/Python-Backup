import requests
from bs4 import BeautifulSoup

URL = 'https://studymaths.co.uk/game.php?gameID=1'
results = requests.get(URL)
doc = BeautifulSoup(results.text,'html.parser')
print(doc.prettify())

questions = doc.find_all(string='register')
print(questions)