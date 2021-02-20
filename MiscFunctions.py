from time import sleep


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
    unit = input("Enter the check frequency unit sec, min, hour, day")
    check_freq = input("Enter the frequency for which you want the product data to be checked in " + unit)

    return check_freq, unit
