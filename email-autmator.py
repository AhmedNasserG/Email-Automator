import os
import getpass
import smtplib 
# from email import encoders
# from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rich.prompt import Confirm
from rich import print
from rich.console import Console
console = Console()

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
    while True:
        path = input("Enter Email Body File Name :")
        extentsion = path.split(".")[-1]
        if not os.path.isfile(path):
            console.print("Sorry, File Does Not Exist, Try Again", style="bold red")
        elif not extentsion in SUPPORTED_EXTENTSION.keys():
            console.print("Sorry, File Is Not Supported, Try Again", style="bold red")
        else:
            break
    with open(path, "r") as f:
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