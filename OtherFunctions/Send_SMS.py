#importing twilio client

from twilio.rest import Client
#Taking Account SID and authentication token from twilio.com

def send_sms(product, price, number):
    account_sid = 'AC2b9b3923e7391dd37e6cf793dde22e3b'
    auth_token = '56a580fdbe1c8d88fdb9768992f55af4'

    client = Client(account_sid, auth_token)
    #Writing a message
    message = client.messages.create(
        from_= '+14124538097',
        to = number,
        body = 'Hi ' + name + ' your product ' + ' '.join(p.split()[0:5]) + ' ...has come down to price of ' + str(price) + '. ' + 'Please check email for url' + '\nDO NOT REPLY'
    )   

    print('SMS sent to: ', number)
