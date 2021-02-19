import requests
from bs4 import BeautifulSoup

url = input("Please enter the url\n")
# url = 'https://www.amazon.in/Infinity-Glide-500-Wireless-Headphones/dp/B07W5MYRF4/ref=sr_1_1_sspa?crid=384417BZYUPRB&dchild=1&keywords=headphone+wireless&qid=1613395289&smid=A14CZOWI0VEHLG&sprefix=headph%2Caps%2C-1&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExVkxNS1MwTkpGUVhWJmVuY3J5cHRlZElkPUEwNzc4NTExMTNTRkVZUTVHRzFTWCZlbmNyeXB0ZWRBZElkPUEwOTM4NDM1M0Y0VVYzUUhEUlhSOCZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='
# url = 'https://www.amazon.com/Sony-MDRZX110-BLK-Stereo-Headphones/dp/B00NJ2M33I/ref=sr_1_3?dchild=1&keywords=headphones&qid=1613717798&sr=8-3'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'close'
}

print("Please wait. we are fetching the data\n\n")

# Get the code of the product page using the url provided
response = requests.get(url, headers=headers)

# code proceeds only if the connection to the product page is successful
if response:
    print("Connected successfully\n\n")
else:
    print("Connection failed")
    exit()

soup = BeautifulSoup(response.content, 'lxml')

# with open('product2.txt', 'w', encoding='utf-8') as f:
#     f.write(soup.prettify())

# Extracting data from the amazon html code
ProductTitle = soup.find(id='productTitle').get_text().strip()
Availability = soup.find(id='availability').get_text().strip()  # In stock.

Price = soup.find(id='price')
# Mrp = int(soup.find(class_='priceBlockStrikePriceString a-text-strike').get_text().strip()[2:-3].replace(',', ''))

DealPrice = None
SellingPrice = None

try:
    DealPrice = int(soup.find(id='priceblock_dealprice').get_text().strip()[2:-3].replace(',', ''))

finally:
    pass

try:
    SellingPrice = int(soup.find(id='priceblock_ourprice').get_text().strip()[2:-3].replace(',', ''))

finally:
    pass

# print(Price.prettify())

print('Product Title: ', ProductTitle)
print('Availability: ', Availability)
print('MRP =', Mrp)

if DealPrice:
    print('Deal Price =', DealPrice)

if SellingPrice:
    print('Selling Price = ', SellingPrice)