import os
import getpass

from rich.prompt import Confirm



def get_credenalties():
    ''' get login credenalties '''
    if not os.path.isfile(".credenalites"):
        username = input("Enter Sender Email : ")
        password = getpass.getpass(prompt="Enter Password : ")
        remember_me = Confirm.ask("Remember me ?")
        if remember_me:
            with open(".credenalites", "w") as f:
                f.write(username+"\n"+password)
    else:
        with open(".credenalites", "r") as f:
            lines = f.readlines()
            username = lines[0].strip()
            password = lines[1].strip()
    return username, password

get_credenalties()