import streamlit as st
st.set_page_config(
    layout="wide",
    page_title="Amazon Product Tracker", 
    page_icon=":tada:"
)

# used to get the data from webpages when url is provided
import requests

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

logging.basicConfig(
    filename='amazon_product_tracker.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a'
)
        
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class AmazonTracker:
    # Constructor of the class it checks if the database file exists, and if it doesn't it creates one
    # and asks for user details and product urls
    def __init__(self, alert_confirmation_email=False, debug=False):

        self.final_price = None
        self.price = None
        self.product_title = None
        self.response = None

        self.alert_confirmation_email = alert_confirmation_email

        st.title("Amazon Product Tracker")
        self.column_1, self.column_2, self.column_3 = st.columns(3)

        self.link = self.column_3.text_input("Add Product link")
        self.maxPrice = self.column_3.number_input("Max Price", 0, 100000)
        self.column_3.button("Add Product", on_click=self.add_product)

        self.column_3.button("Remove Products", on_click=self.remove_products)

        self.debug = debug

        logger.info('Starting Amazon Product Tracker...')
        logger.info('Connecting to sql database')
        try:
            self.db = Database()
        except Exception as e:
            logger.critical(e, exc_info=True)
            exit()

        self.db.clear_recent_products()

        params = self.db.access_product_params()
        self.name, self.to_addr, self.number, self.check_freq = self.db.access_user_data()
        self.check_freq = float(self.check_freq)

        for param in params:
            self.product_data = ''
            self.product_id = param[0]
            self.url = param[1]
            self.maxPrice = int(param[2])

            success = False
            while not success:
                try:
                    logger.info('Connecting to ' + self.url)
                    self.connect()
                    res = self.extract_data()

                    if not res:
                        continue

                    self.send_alert()
                    success = True
                except Exception as e:
                    logger.critical(e, exc_info=True)
                    sleep(5)
            
        self.db.close()

    def __del__(self):
        self.db.close()

    def add_product(self):
        self.db.get_product_params(self.link, self.maxPrice)
        self.link = ''
        self.column_3.info("Product added")
    
    def remove_products(self):
        for i in st.session_state.keys():
            if st.session_state[i] == True:
                self.db.remove_product(i)

        self.column_3.info("Products removed")

    # connects to the webpage provided using the url
    def connect(self):
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
                logger.info('Connected to ' + self.url)
        else:   
            logger.critical("Connection failed. Response code: " + str(self.response.status_code), exc_info=True)
            exit()

    # After the web page data is obtained the required data such as the product price is extracted.
    def extract_data(self):
        soup = BeautifulSoup(self.response.content, 'lxml')

        price = None

        # Extracting data from the amazon html code
        try:
            self.product_title = soup.find(id='productTitle').get_text().strip()
            availability = soup.find(id='availability') # In stock.
        except:
            logger.error("Product not found", self.url, exc_info=True)
            return False

        try:
            availability = availability.get_text().strip() 
        except AttributeError:
            availability = None

        # Get the price of the product
        try:
            if not price:
                classes = ['a-price-whole']
                for class__ in classes:
                    price = soup.find('span', {'class': class__})
                    if price:
                        price = price.get_text().strip().replace(',', '').replace('.', '')
                        break
        except AttributeError as e:
            logger.error()

        # Get the average rating of the product
        try:
            rating = soup.find('span', {'class': 'a-icon-alt'}).get_text().strip().split(' ')[0]
        except AttributeError:
            rating = None

        # Get the number of ratings of the product
        try:
            num_ratings = soup.find('span', {'id': 'acrCustomerReviewText'}).get_text().strip().replace(',', '').split(' ')[0]
        except AttributeError:
            num_ratings = None

        self.product_data+=f'{self.product_title}\n'
        self.product_data+=f'Availability: {availability}\n'

        if price:
            self.final_price = int(price)
            self.product_data+=f'\tPrice = {price}\n'
        else:
            self.product_data+='\tPrice = Not available'

        self.product_data+=f'\tMax price set by user = {self.maxPrice}\n'

        self.db.update_recent_products(self.product_title, self.final_price, availability, rating, num_ratings, self.url)

        self.column_1.checkbox(label="", key=self.product_id)
        self.column_2.write(self.product_data)

        return True

    # Send alert to the user if price falls below the max price set by the user.
    def send_alert(self):
        try:
            if self.final_price and self.final_price <= self.maxPrice:
                self.db.insert_alert(self.product_title, self.final_price, self.url)
                if self.alert_confirmation_email:
                    logger.info('Sending email to ' + self.to_addr)
                    send_mail(self.to_addr, self.name, self.product_title, self.final_price, self.url)
        except AttributeError:
            self.product_data+="\n\tERROR: Could not access the price of the product"
            logger.error("Could not access the price of the product", exc_info=True)


AmazonTracker(alert_confirmation_email=False)
