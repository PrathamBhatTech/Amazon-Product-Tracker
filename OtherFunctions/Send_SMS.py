#importing twilio client

from twilio.rest import Client
import os
#Taking Account SID and authentication token from twilio.com

def send_sms(number):
    account_sid = 'AC2b9b3923e7391dd37e6cf793dde22e3b'
    auth_token = '73e05c2e1af8d22379cb305d0d55cddd'

    client = Client(account_sid, auth_token)

    #Writing a message

    message = client.messages.create(
        from_= '+14124538097',
        to = '+919342581008',
        body = 'Your amazon product is tracked'
    )   

    #print(message.sid)

send_sms(number = '+919342581008')
