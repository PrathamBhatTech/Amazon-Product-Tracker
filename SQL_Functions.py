# used to check if a given file exists or not
import os.path

# used to create, modify and store database files using sql
import sqlite3 as sql

# miscellaneous functions that are repeated but simple
from MiscFunctions import *


class Database:
    def __init__(self):
        # If the file does not exist then create one and ask user for email and check frequency
        if not self.file_exists():
            self.connect()
            self.create_tables()
            # self.get_user_data()
        else:
            self.connect()

    '''
        These functions will get data from user and store it in the database
    '''

    # Checks if a given file exists
    @staticmethod
    def file_exists():
        if os.path.isfile('Database.db'):
            return True
        else:
            return False

    # Attempts connection to the database file
    def connect(self):
        try:
            self.con = sql.connect('Database.db')
        except sql.Error:
            print(sql.Error)
            exit()

        # Create a cursor using the connection to the database
        self.c = self.con.cursor()

    # Create tables url and user for first time initialization
    def create_tables(self):
        self.c.execute('CREATE TABLE URL(url, maxPrice, availabilityAlertEmail, availabilityAlertNotification)')
        self.c.execute('CREATE TABLE USER(username, email, checkFrequency)')

    # Gets the user data from user
    def get_user_data(self):
        username = input('Enter your name')
        email = get_email()
        check_freq, unit = get_check_freq()

        self.c.execute('INSERT INTO USER VALUES(?, ?, ?)', (username, email, check_freq))

        self.con.commit()

    def get_product_params(self):
        url = input('Copy the url from the product page and paste it below\n')
        max_price = input('Enter the max price of the product')
        availability_alert_email = input('Enter true for false if you want to get an'
                                         ' email alert when the price of the product falls below the max price')
        availability_alert_notification = input('Enter true for false if you want to get an notification alert when'
                                                ' the price of the product falls below the max price')

        self.c.execute('INSERT INTO URL VALUES(?, ?, ?, ?)',
                       (url, max_price, availability_alert_email, availability_alert_notification))

        self.con.commit()

    '''
        From here the functions will access the database to return values
    '''

    def access_user_data(self):
        user = self.c.execute("SELECT * FROM USER").fetchone()
        return user

    def access_product_params(self):
        params = self.c.execute("SELECT * FROM URL").fetchall()
        return params
