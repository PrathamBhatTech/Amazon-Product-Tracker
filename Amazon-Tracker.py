import requests
from bs4 import BeautifulSoup
from os import name, system


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


url = input("Please enter the url\n")

# The headers are used to make the code imitate a browser and prevent amazon from block it access to the site.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'close'
}

print("Please wait. We are attempting to connect to the product page\n\n")

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

except:
    pass

try:
    SellingPrice = int(soup.find(id='priceblock_ourprice').get_text().strip()[2:-3].replace(',', ''))

except:
    pass

# Clear the screen
clear()

# ReviewScore = float(soup.select('.a-star-4-5')[0].get_text().split()[0].replace(',', '.'))

# print(Price.prettify())

print('Product Title: ', ProductTitle)
print('Availability: ', Availability)
# print('MRP =', Mrp)

if DealPrice:
    print('Deal Price =', DealPrice)

if SellingPrice:
    print('Selling Price = ', SellingPrice)

# print(ReviewScore)