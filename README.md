# Amazon Tracker

The <b>Amazon Tracker</b> stores the urls entered by the user and the email of the user and checks all the urls.
When the price falls below the max price an email and notification is sent to the user.

User Manual:

    > cd into the directory of the project and type: pip install -r requirements.txt
      This will install all the required libraries.

    > Click on Amazon-Tracker.py and fill in the data asked.

    > Whenever you want to check the products just click on this file.

    > If you want to add new products or remove products later on, click on Product_Manager.py
      and follow the instructions.

Contributors:

    Pratham Bhat
        > Storing urls, email, names and max price of products using sql
        > Accessing html product data using requests
        > Processing html to get information such as price and product title
        > Sending email if price drops below the threshold
        > CUI for adding and removing urls

    Prateek Pangal Rao
        > Sending SMS to user's phone for price drop alerts
