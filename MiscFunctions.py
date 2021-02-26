from time import sleep

# used to clear the terminal window
from os import name, system


# Verifies if the email has at least a basic resemblance to an email
def get_email():
    while True:
        email = input("Please enter your email for alert notifications")
        if '@' not in email or '.' not in email or len(email) < 6:
            print('Error: Please enter a valid email')
            sleep(2)
        else:
            return email


def get_check_freq():
    unit = input("Enter the check frequency unit sec, min, hour, day\n")
    check_freq = input("Enter the frequency for which you want the product data to be checked in " + unit + '\n')

    return check_freq  # , unit


# TODO Remove the _ = if clear is used and see if it woks.
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
