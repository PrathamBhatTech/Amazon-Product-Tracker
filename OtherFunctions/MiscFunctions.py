from time import sleep

# used to clear the terminal window
from os import name, system


# Verifies if the email has at least a basic resemblance to an email
def get_email():
    while True:
        email = input("Please enter your email for alert notifications: ")
        if '@' not in email or '.' not in email or len(email) < 6:
            print('Error: Please enter a valid email')
            sleep(2)
        else:
            return email


def get_number():
    while True:
        number = input("Please enter your phone number for alert notifications: ")
        if len(number) != 10:
            print('Error: Please input valid phone number')
            sleep(2)
        else:
            return '+91' + number


# Gets the frequency for which the program should run.
def get_check_freq():
    return input("Enter the frequency for which you want the product data to be checked in minutes"
                 "(Decimals allowed)\n")


# Used to clear the terminal window
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
