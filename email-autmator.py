import os
import getpass
import sys

import smtplib 
# from email import encoders
# from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyInquirer import prompt

from rich.prompt import Confirm
from rich import print
from rich.console import Console
from rich.panel import Panel

console = Console()

def showMenu(title, options):
    questions = {
                'type': 'list',
                'name': 'theme',
                'message': title,
                'choices': options
    }
    while (True):
        terminal_menu = prompt(questions)
        if len(list(terminal_menu.values())) != 0:
            break
    return list(terminal_menu.values())[0]

def get_credenalties():
    ''' get login credenalties '''
    if not os.path.isfile(".credenalites"):
        sender_email = input("Enter Sender Email : ")
        password = getpass.getpass(prompt="Enter Password : ")
        remember_me = Confirm.ask("Remember me ?")
        if remember_me:
            with open(".credenalites", "w") as f:
                f.write(sender_email+"\n"+password)
    else:
        with open(".credenalites", "r") as f:
            lines = f.readlines()
            sender_email = lines[0].strip()
            password = lines[1].strip()
    return sender_email, password


def get_mail_content():
    SUPPORTED_EXTENTSION = {"txt" : "plain","html" :"html"}
    supported_files = [f for f in os.listdir() if f.split(".")[-1] in SUPPORTED_EXTENTSION.keys()]
    if len(supported_files) == 0:
        console.print(Panel(f'''[red]Sorry, There are not any Supported Files in Email-Autmator Directory [/red]
We support {str(list(SUPPORTED_EXTENTSION.keys()))[1:-1]}.
If you need other types add an issue on Github: https://github.com/AhmedNasserG and we will add them ASAP
Please Add One And Try Again''', style="bold"))
        sys.exit()
    file = showMenu("Select Email Body File :", supported_files)
    extentsion = file.split(".")[-1]
    with open(file, "r") as f:
        message = MIMEMultipart()
        message.attach(MIMEText(f.read(), SUPPORTED_EXTENTSION[extentsion]))
    return message

def send_mail(receiver_emails, message):
    ''' send a mail to a group of emails '''
    sender_email, password = get_credenalties()
    s = smtplib.SMTP("smtp.gmail.com", 587) 
    s.starttls() 
    s.login(sender_email, password) 
    for receiver_email in receiver_emails:
        s.sendmail(sender_email, receiver_email, message.as_string()) 
    s.quit()


# test
receiver_emails, email = ["ahmednasser21731@yahoo.com"], get_mail_content()
send_mail(receiver_emails, email)
# print("done")
# get_mail_content()
