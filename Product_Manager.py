from OtherFunctions.SQL_Functions import Database

from Amazon_Tracker import AmazonTracker

from OtherFunctions.MiscFunctions import clear

while KeyboardInterrupt:
    # This tells the constructor to disable alerts
    AT = AmazonTracker(loop=False)

    option = input('1: Add products\n'
                   '2: Remove products\n'
                   '3: Exit\n')

    db = Database()
    if option == '1':
        db.get_product_params()
    elif option == '2':
        print("Enter the Product ID of the product you want deleted\nTo remove multiple products enter them separated by a space")

        product_ids = input().split(' ')
        for product_id in product_ids:
            db.remove_product(int(product_id))
    elif option == '3':
        exit()

    clear()
