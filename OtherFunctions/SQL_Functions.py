# used to check if a given file exists or not
import os.path

# used to create, modify and store database files using sql
import sqlite3 as sql

# miscellaneous functions that are repeated but simple
from OtherFunctions.MiscFunctions import *


class Database:
    def __init__(self):
        # If the file does not exist then create one and ask user for email and check frequency
        self.c = None
        self.con = None

        self.database_path = "Assets/Database.db"

        if not self.file_exists():
            self.connect()
            self.create_tables()
            self.get_user_data()
            self.get_product_params()

        else:
            self.connect()

    '''
        These functions will get data from user and store it in the database
    '''

    # Checks if a given file exists
    def file_exists(self):
        if os.path.isfile(self.database_path):
            return True
        else:
            return False

    # Attempts connection to the database file
    def connect(self):
        try:
            self.con = sql.connect(self.database_path)
        except sql.Error:
            print(sql.Error)
            exit()

        # Create a cursor using the connection to the database
        self.c = self.con.cursor()

    # Create tables url and user for first time initialization
    def create_tables(self):
        self.c.execute('CREATE TABLE URL(product_id, url, maxPrice)')
        self.c.execute('CREATE TABLE USER(username, email, number, checkFrequency)')

    # Gets the user data from user
    def get_user_data(self):
        username = input('Enter your name: ')
        email = get_email()
        number = get_number()
        check_freq = get_check_freq()

        self.c.execute('INSERT INTO USER VALUES(?, ?, ?, ?)', (username, email, number, check_freq))

        self.con.commit()

    def get_product_params(self):
        while True:
            url = input('Copy the url from the product page and paste it below\n')
            max_price = input('Enter the max price of the product\n')

            product_id = len(self.c.execute("SELECT product_id FROM URL").fetchall()) + 1
            if self.c.execute("SELECT product_id FROM URL").fetchone() == "1":
                product_id -= 1

            # Insert the received values into the sql database
            self.c.execute('INSERT INTO URL VALUES(?, ?, ?)',
                           (product_id, url, max_price))

            # commits the changes made to the database
            self.con.commit()

            print('\n\nDo you want to enter another product link? y/n\n')

            # If the user doesn't enter y then the url access function is terminated.
            if input() != 'y':
                break

    '''
        From here the functions will access the database to return values
    '''

    def access_user_data(self):
        return self.c.execute("SELECT * FROM USER").fetchone()

    def access_product_params(self):
        return self.c.execute("SELECT * FROM URL").fetchall()

    def remove_product(self, product_id):
        self.c.execute("DELETE FROM URL WHERE product_id = " + str(product_id))
        print("The product has been removed")
        self.rearrange_products(int(product_id))

    def rearrange_products(self, deleted_product_id):
        for i in range(deleted_product_id, len(self.c.execute("SELECT product_id FROM URL").fetchall()) + 2):
            self.c.execute("UPDATE URL SET product_id = ? WHERE product_id = ?", (i - 1, i))
        self.con.commit()
