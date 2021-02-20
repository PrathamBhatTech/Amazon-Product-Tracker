import os.path

import sqlite3 as sql

from MiscFunctions import *


class GetURL:
    def __init__(self):
        if not self.file_exists():
            self.connect()
            self.create_tables()
            self.get_user_data()
        else:
            self.connect()

    @staticmethod
    def file_exists(self):
        if os.path.isfile('Database.db'):
            return True
        else:
            return False

    def connect(self):
        try:
            self.con = sql.connect('Database.db')
        except sql.Error:
            print(sql.Error)
            exit()

        self.c = self.con.cursor()

    def create_tables(self):
        self.c.execute('CREATE TABLE URL(url, maxPrice, availabilityAlertEmail, availabilityAlertNotification)')
        self.c.execute('CREATE TABLE USER(username, email, checkFrequency)')

    def get_user_data(self):
        username = input('Enter your name')
        email = get_email()
        checkfreq, unit = get_check_freq()

        self.c.execute('INSERT INTO TABLE USER(username, email, checkfreq, unit)')

    def get_product_params(self):
        url = input('Copy the url from the product page and paste it below\n')
        maxPrice = input('Enter the max price of the product')
        availabilityAlertEmail = input('Enter true for false if you want to get an'
                                       ' email alert when the price of the product falls below the max price')
        availabilityAlertNotification = input('Enter true for false if you want to get an notification alert when'
                                              ' the price of the product falls below the max price')

        self.c.execute('INSERT INTO TABLE URL(url, maxPrice, availabilityAlertEmail, availabilityAlertNotification)')
