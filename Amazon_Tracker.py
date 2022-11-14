# used to get the data from webpages when url is provided
import requests

# import app
import app as app

# used to delay the code
from time import sleep

# log data
import logging

# Used to parse data provided by requests to extract the data required
from bs4 import BeautifulSoup

# miscellaneous functions that are repeated but simple
from OtherFunctions.MiscFunctions import *

# Import the sql functions that access database
from OtherFunctions.SQL_Functions import Database

# Import functions to send mail
from OtherFunctions.Send_Email import send_mail

# Import module to send sms
# from OtherFunctions.Send_SMS import send_sms


logging.basicConfig(
    filename='$Home/amazon_product_tracker.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a'
)
        
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class AmazonTracker:
    # Constructor of the class it checks if the database file exists, and if it doesn't it creates one
    # and asks for user details and product urls
    def __init__(self, alert_confirmation_email=False, alert_confirmation_sms=False, loop=True, debug=False):

        self.final_price = None
        self.price = None
        self.product_title = None
        self.response = None

        self.alert_confirmation_email = alert_confirmation_email
        self.alert_confirmation_sms = alert_confirmation_sms

        while KeyboardInterrupt:
            self.debug = debug

            params = db.access_product_params()
            self.name, self.to_addr, self.number, self.check_freq = db.access_user_data()
            self.check_freq = float(self.check_freq)
            for param in params:
                self.product_id = param[0]
                self.url = param[1]
                self.maxPrice = int(param[2])

                success = False
                while not success:
                    try:
                        self.product_data = ''
                        logger.info('Connecting to ' + self.url)
                        self.connect()
                        self.extract_data()

                        self.send_alert()
                        success = True
                    except Exception as e:
                        #self.product_data+=e
                        logger.critical(e, exc_info=True)
                        #self.product_data+="Unable to connect to Amazon. Retrying in 1 minute"
                        sleep(60)

            #self.product_data+='\n\nAll products have been checked\n'
            #self.product_data+=f'Waiting for {self.check_freq} minutes before checking again\n\n'

            if not loop:
                break

            self.product_data+='Enter ctrl + c to exit code'

            sleep(self.check_freq * 60)  # Stops the code process for the time specified in the parameter
        

    # connects to the webpage provided using the url
    def connect(self):
        # if self.debug:
            #self.product_data+="\n\nPlease wait. We are attempting to connect to the product page"

        # The headers are used to make the code imitate a browser and prevent amazon from blocking it access to the
        # site.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/'
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
                self.product_data+="Connected successfully\n\n"
        else:   
            #self.product_data+="Connection failed"
            logger.critical("Connection failed. Response code: " + str(self.response.status_code), exc_info=True)
            exit()

    # After the web page data is obtained the required data such as the product price is extracted.
    def extract_data(self):
        soup = BeautifulSoup(self.response.content, 'lxml')

        price = None

        # Extracting data from the amazon html code
        self.product_title = soup.find(id='productTitle').get_text().strip()
        availability = soup.find(id='availability') # In stock.

        try:
            availability = availability.get_text().strip() 
        except AttributeError:
            availability = None

        # Get the price of the product
        try:
            # ids = ['priceblock_ourprice', 'a-price', 'a-price-whole']

            # for id__ in ids:
            #     price = soup.find(id=id__) 

            #     if price:
            #         price = price.get_text().strip()
            #         break
                
            if not price:
                classes = ['a-price-whole']
                for class__ in classes:
                    price = soup.find('span', {'class': class__})
                    if price:
                        price = price.get_text().strip().replace(',', '').replace('.', '')
                        break
        except AttributeError as e:
            self.product_data+=e

        #self.product_data+=f"\nProduct ID: {self.product_id}"
        self.product_data+=f'\tProduct Title: {self.product_title}'
        self.product_data+=f'\tAvailability: {availability}'

        if price:
            self.final_price = int(price)
            self.product_data+=f'\tPrice = {price}'
        else:
            self.product_data+='\tPrice = Not available'

        self.product_data+=f'\tMax price set by user = {self.maxPrice}'

        app.print(self.product_id, self.product_title, self.product_data)

    # Send alert to the user if price falls below the max price set by the user.
    def send_alert(self):
        try:
            if self.final_price and self.final_price <= self.maxPrice:
                if self.alert_confirmation_email:
                    logger.info('Sending email to ' + self.to_addr)
                    send_mail(self.to_addr, self.name, self.product_title, self.final_price, self.url)
                if self.alert_confirmation_sms:
                    logger.info('Sending sms to ' + self.number)
                    send_sms(self.name, self.product_title, self.final_price, self.number)
        except AttributeError:
            self.product_data+="\n\tERROR: Could not access the price of the product"
            logger.error("Could not access the price of the product", exc_info=True)


logger.info('Starting Amazon Product Tracker...')
logger.info('Connecting to sql database')
try:
    db = Database()
except Exception as e:
    self.product_data+=e
    logger.critical(e, exc_info=True)
    exit()

AmazonTracker(alert_confirmation_email=False, alert_confirmation_sms=False)
