#importing twilio client

from twilio.rest import Client

#Taking Account SID and authentication token from twilio.com

account_sid = 'AC2b9b3923e7391dd37e6cf793dde22e3b'
auth_token = 'c873b6301629c94ea63f50ba2bec0818'

client = Client(account_sid, auth_token)

#Writing a message

message = client.messages.create(
    from_= '+14124538097',
    to = '+919342581008',
    body = 'This is a test for python sms'
)
