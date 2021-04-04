# used to get the data from webpages when url is provided
import requests

# used to delay the code
# from time import sleep

# Used to parse data provided by requests to extract the data required
from bs4 import BeautifulSoup

# miscellaneous functions that are repeated but simple
from OtherFunctions.MiscFunctions import *

# Import the sql functions that access database
from OtherFunctions.SQL_Functions import Database

from OtherFunctions.Send_Email import send_mail

# Import module to send sms
from OtherFunctions.Send_SMS import send_sms


class AmazonTracker:
    # Constructor of the class it checks if the database file exists, and if it doesn't it creates one
    # and asks for user details and product urls
    def __init__(self, alert_confirmation_email=False, alert_confirmation_sms=False, loop=True, debug=False):
        self.alert_confirmation_email = alert_confirmation_email
        self.alert_confirmation_sms = alert_confirmation_sms

        print('Accessing product data. If you are tracking many products this may take a while.')
        while KeyboardInterrupt:
            self.debug = debug

            params = db.access_product_params()
            self.name, self.to_addr, self.number, self.check_freq = db.access_user_data()
            self.check_freq = float(self.check_freq)
            for param in params:
                self.product_id = param[0]
                self.url = param[1]
                self.maxPrice = int(param[2])

                self.connect()
                self.extract_data()

                self.send_alert()

            print('\n\nAll products have been checked\n')

            if not loop:
                break

            print('Enter ctrl + c to exit code')

            sleep(self.check_freq * 60)  # Stops the code process for 20 seconds

    # connects to the webpage provided using the url
    def connect(self):
        if self.debug:
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
            if self.debug:
                print("Connected successfully\n\n")
        else:
            print("Connection failed")
            exit()

    # After the web page data is obtained the required data such as the product price is extracted.
    def extract_data(self):
        soup = BeautifulSoup(self.response.content, 'lxml')

        deal_price = None
        price = None

        # Extracting data from the amazon html code
        self.product_title = soup.find(id='productTitle').get_text().strip()
        availability = soup.find(id='availability').get_text().strip()  # In stock.

        self.price = soup.find(id='price')

        # Exception handling is used to prevent the code from crashing if the required data is missing
        try:
            deal_price = int(soup.find(id='priceblock_dealprice').get_text().strip()[2:-3].replace(',', ''))

        except AttributeError:
            pass

        try:
            price = int(soup.find(id='priceblock_ourprice').get_text().strip()[2:-3].replace(',', ''))

        except AttributeError:
            pass

        print("\nProduct ID: ", self.product_id)
        print('\tProduct Title: ', self.product_title)
        print('\tAvailability: ', availability)

        # Print the data if it is found in the code
        if deal_price:
            print('\tDeal Price =', deal_price)
            self.final_price = deal_price

        if price:
            if type(self.price) == "<class 'bs4.element.Tag'>":
                self.final_price = deal_price
            else:
                self.final_price = price
                print('\tPrice = ', price)

        print('\tMax price set by user = ', self.maxPrice)

    # Send alert to the user if price falls below the max price set by the user.
    def send_alert(self):
        try:
            if self.final_price <= self.maxPrice:
                if self.alert_confirmation_email:
                    send_mail(self.to_addr, self.name, self.product_title, self.final_price, self.url)
                if self.alert_confirmation_sms:
                    send_sms(self.name, self.product_title, self.final_price, self.number)
        except AttributeError:
            print("\n\tERROR: Could not access the price of the product")


db = Database()
if __name__ == '__main__':
    # The one is telling the constructor to enable user alerts.
    AmazonTracker(alert_confirmation_email=True, alert_confirmation_sms=False)
