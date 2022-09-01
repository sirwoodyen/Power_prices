import os


def clear_screen():

    # It is for MacOS and Linux(here, os.name is 'posix')
    if os.name == 'posix':
        os.system('clear')
    else:
        # It is for Windows platfrom
        os.system('cls')