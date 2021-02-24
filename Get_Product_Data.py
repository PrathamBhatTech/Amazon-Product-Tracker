from SQL_Functions import Database

url = input("Please enter the url of the product")
maxPrice = input("Please enter the maximum price of the product")
availabilityAlertEmail = True
availabilityAlertNotification = False

Database.insert_product_data(url, maxPrice, availabilityAlertEmail, availabilityAlertNotification)
