#importing twilio 

from twilio.rest import Client

#Account_SID & Authentication token taken from Twilio Console

account_sid = 'AC2b9b3923e7391dd37e6cf793dde22e3b'
auth = 'c873b6301629c94ea63f50ba2bec0818'

client = Client(account_sid, auth)

#Creating a message:

message = client.messages.create(
    from_= '+14124538097',
    to = '+919342581008',
    body = 'Testing for Amazon Tracking Project'
)

print(message.sid)
