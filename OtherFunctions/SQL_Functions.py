# used to check if a given file exists or not
import os.path

# used to create, modify and store database files using sql
import sqlite3 as sql
# import mysql.connector as sql

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
        self.c.execute('CREATE TABLE URL(product_id NOT NULL, url PRIMARY KEY, maxPrice NOT NULL)')
        self.c.execute('CREATE TABLE USER(username PRIMARY KEY, email UNIQUE NOT NULL, number UNIQUE, checkFrequency NOT NULL)')
        self.c.execute('CREATE TABLE PRODUCTS(name PRIMARY KEY, price, availability, rating, number_of_ratings, link, FOREIGN KEY (link) REFERENCES URL(url))')
        self.c.execute('CREATE TABLE ALERTS(timestamp, link VARCHAR(1000));')

        self.c.execute('''CREATE TRIGGER buy_alert 
                        AFTER INSERT ON PRODUCT
                        FOR EACH ROW 
                        IF NEW.price > (SELECT maxPrice FROM URL WHERE url = NEW.link)
                        INSERT INTO ALERTS (CURRENT_TIMESTAMP, NEW.name, NEW.price, NEW.availability, NEW.rating, NEW.number_of_ratings, NEW.url)
        ''')

    # Gets the user data from user
    def get_user_data(self):
        username = input('Enter your name: ')
        self.email = get_email()
        number = get_number()
        check_freq = get_check_freq()

        self.c.execute('INSERT INTO USER VALUES(?, ?, ?, ?)', (username, self.email, number, check_freq))

        self.con.commit()

    def get_product_params(self, url=None, max_price=None):
        product_id = self.c.execute('SELECT COUNT(*) FROM URL').fetchone()[0] + 1
        # Insert the received values into the sql database
        self.c.execute('INSERT INTO URL VALUES(?, ?, ?)',
                    (product_id, url, max_price))

        # commits the changes made to the database
        self.con.commit()

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

    def update_recent_products(self, name, price, availability, rating, num_ratings, url):
        self.c.execute("INSERT INTO PRODUCTS VALUES(?, ?, ?, ?, ?, ?)", (name, price, availability, rating, num_ratings, url))
        self.con.commit()

    def insert_alert(self, timestamp, link):
        self.c.execute("INSERT INTO ALERTS VALUES(?, ?, ?)", (timestamp, self.email, link))
        self.con.commit()

    def get_alerts(self):
        return self.c.execute("SELECT * FROM ALERTS").fetchall()

    def clear_alerts(self):
        self.c.execute("DELETE FROM ALERTS")
        self.con.commit()

    def get_analysis(self):
        return self.c.execute("SELECT COUNT(*), SUM(price), MAX(price), AVG(rating), SUM(number_of_ratings) FROM PRODUCTS").fetchone()

    def clear_recent_products(self):
        self.c.execute("DELETE FROM PRODUCTS")
        self.con.commit()

    def run_query(self, query):
        return self.c.execute(query).fetchall()

    def close(self):
        self.con.close()