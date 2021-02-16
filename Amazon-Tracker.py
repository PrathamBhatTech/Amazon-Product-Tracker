import requests
import selectorlib
from bs4 import BeautifulSoup

# url = input("Please enter the url\n")
url = 'https://www.amazon.in/Infinity-Glide-500-Wireless-Headphones/dp/B07W5MYRF4/ref=sr_1_1_sspa?crid=384417BZYUPRB&dchild=1&keywords=headphone+wireless&qid=1613395289&smid=A14CZOWI0VEHLG&sprefix=headph%2Caps%2C-1&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExVkxNS1MwTkpGUVhWJmVuY3J5cHRlZElkPUEwNzc4NTExMTNTRkVZUTVHRzFTWCZlbmNyeXB0ZWRBZElkPUEwOTM4NDM1M0Y0VVYzUUhEUlhSOCZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'close'
}

#headers={'User-Agent': 'Defined'}

# Get the code of the product page using the url provided
response = requests.get(url, headers=headers)

print(response)

# code proceeds only if the connection to the product page is successful
if response:
    print("Connected successfully")
else:
    print("Connection failed")
    exit()

soup = BeautifulSoup(response.content, 'html.parser').encode('utf-8 ')
with open('product.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)
