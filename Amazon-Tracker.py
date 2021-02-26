# used to get the data from webpages when url is provided
import requests

# Used to parse data provided by requests to extract the data required
from bs4 import BeautifulSoup

# used to delay the code for a set amount of time

# miscellaneous functions that are repeated but simple
from OtherFunctions.MiscFunctions import *

# Import the sql functions that access database
from OtherFunctions.SQL_Functions import Database

from OtherFunctions.Send_Email import send_mail


class AmazonTracker:

    # Constructor of the class it checks if the database file exists, and if it doesn't it creates one
    # and asks for user details and product urls
    def __init__(self):
        params = db.access_product_params()
        for param in params:
            self.url = param[0]
            self.maxPrice = int(param[1])
            self.connect()
            self.extract_data()

    # connects to the webpage provided using the url
    def connect(self):
        print("\n\nPlease wait. We are attempting to connect to the product page")

        # The headers are used to make the code imitate a browser and prevent amazon from block it access to the site.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'close'
        }

        # Get the code of the product page using the url provided
        self.response = requests.get(self.url, headers=headers)

        # code proceeds only if the connection to the product page is successful
        if self.response:
            print("Connected successfully\nProcessing data. Please wait\n\n")
        else:
            print("Connection failed")
            exit()

    # After the web page data is obtained the required data such as the product price is extracted.
    def extract_data(self):
        soup = BeautifulSoup(self.response.content, 'lxml')

        # with open('product2.txt', 'w', encoding='utf-8') as f:
        #     f.write(soup.prettify())

        # Extracting data from the amazon html code
        product_title = soup.find(id='productTitle').get_text().strip()
        availability = soup.find(id='availability').get_text().strip()  # In stock.

        price = soup.find(id='price')
        # Mrp = int(soup.find(class_='priceBlockStrikePriceString a-text-strike').get_text().strip()[2:-3].replace(',', ''))

        deal_price = None
        selling_price = None

        # Exception handling is used to prevent the code from crashing if the required data is missing
        try:
            deal_price = int(soup.find(id='priceblock_dealprice').get_text().strip()[2:-3].replace(',', ''))

        except:
            pass

        try:
            price = int(soup.find(id='priceblock_ourprice').get_text().strip()[2:-3].replace(',', ''))

        except:
            pass

        # Clear the screen
        # clear()

        # ReviewScore = float(soup.select('.a-star-4-5')[0].get_text().split()[0].replace(',', '.'))

        # print(Price.prettify())

        print('Product Title: ', product_title)
        print('Availability: ', availability)
        # print('MRP =', Mrp)

        # Print the data if it is found in the code
        if deal_price:
            print('Deal Price =', deal_price)

        if price:
            print('Price = ', price)

        name, to_addr, checkFreq = db.access_user_data()

        print(self.maxPrice)
        if price <= self.maxPrice:
            send_mail(to_addr, name, product_title, price, self.url)


# after the code runs once a break of 20 seconds is given before running again
while KeyboardInterrupt:
    db = Database()
    AmazonTracker()

    print('All products have been checked\n')
    print('Enter ctrl + c to exit code')

    sleep(20)  # Stops the code process for 20 seconds
