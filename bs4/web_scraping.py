from bs4 import BeautifulSoup
import requests

url_zotac = 'https://www.newegg.com/zotac-geforce-rtx-4090-zt-d40900j-10p/p/1FT-000M-003C8?Description=4090&cm_re=4090-_-1FT-000M-003C8-_-Product'

zotac_result = requests.get(url_zotac)
zotac_doc = BeautifulSoup(zotac_result.text, 'html.parser')
zotac_prices = zotac_doc.find_all(text = '$')
zotac_parent = zotac_prices[0].parent

zotac_price = zotac_parent.findChildren('strong', recursive = 'False')