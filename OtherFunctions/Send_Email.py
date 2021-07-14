import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(to_addr, name, product, price, product_link):
    # username and password of the mail.
    username, password = 'python.smtp.pbtron@gmail.com', 'python123$'

    # Create a server. 25 is the port. port is 25 for smtp.
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Initiate the service
    server.ehlo()
    server.starttls()

    # login
    server.login(username, password)

    # Create a multi message
    msg = MIMEMultipart()

    msg['From'] = username
    msg['To'] = to_addr
    msg['Subject'] = "Price Drop"

    # Getting the text from the text file and adding it to the text
    with open('OtherFunctions/mail_message.md', 'r+') as f:
        message = f.read().format(name, product, price, product_link)

    msg.attach(MIMEText(message, 'plain'))

    # Convert the text to string
    text = msg.as_string()

    server.sendmail(username, to_addr, text)

    print("Mail Sent to ", to_addr)
