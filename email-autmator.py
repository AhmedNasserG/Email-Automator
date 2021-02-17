import os
import getpass
import sys
import csv

import smtplib 
# from email import encoders
# from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyInquirer import prompt

from rich.prompt import Confirm, Prompt 
from rich import print
from rich.console import Console
from rich.panel import Panel

# TODO: Fix can't close the script when the menu is shown
# TODO: Add Auth method
# TODO: handel empty menu , add select file method


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

def show_checklist(title, options):
    questions = [
    {
        'type': 'checkbox',
        'message': title,
        'name': 'emails',
        'choices': [dict(zip(['name'],[op])) for op in options]
    }
    ]
    choices = prompt(questions)
    return [options.index(i) for i in choices['emails']]

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
        console.print(Panel(f'''[red]Sorry, There are not any Supported Files in Current Directory [/red]
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

def preview_emails(receiver_emails):
    console.print(f"There are {len(receiver_emails)} Added Receiver Emails", style="bold yellow")
    for i, email in enumerate(receiver_emails):
        console.print(f"([bold magenta]{i+1}[/bold magenta]) {email}")

def edit_emails(receiver_emails):
    selected_emails = show_checklist("Select Emails to Edit", receiver_emails)
    for i in selected_emails:
        receiver_emails[i] = Prompt.ask(f"Edit [bold blue]{receiver_emails[i]}[/bold blue] to ")

def delete_emails(receiver_emails):
    selected_emails = show_checklist("Select Emails to Delete", receiver_emails)
    receiver_emails[:] = [email for i, email in enumerate(receiver_emails) if i not in selected_emails]

def add_emails(receiver_emails):
    user_input = Prompt.ask("Write Receiver Emails Seperated with spaces ")
    receiver_emails += user_input.split()
    console.print(f"Successfully added {len(user_input.split())} Emails, Total Number of Emails is {len(receiver_emails)}", style="bold green")

def preprocess_emails(receiver_emails):
    while True:
        mod = Prompt.ask(f"There are [bold blue]{len(receiver_emails)}[/bold blue] Emails Added, Want to :",
            choices=["submit", "preview", "edit", "delete", "add"], default="submit")
        if mod == "preview":
            preview_emails(receiver_emails)
        elif mod == "edit":
            edit_emails(receiver_emails)
        elif mod == "delete":
            delete_emails(receiver_emails)
        elif mod == "add":
            add_emails(receiver_emails)
        elif mod == "submit":
            break

def get_receiver_emails_manual():
    receiver_emails = []
    add_emails(receiver_emails)
    preprocess_emails(receiver_emails)
    return receiver_emails

def get_receiver_emails_txt(file):
    receiver_emails = []
    with open(file, mode="r") as txt_file:
        receiver_emails = txt_file.read().split()
    preprocess_emails(receiver_emails)
    return receiver_emails

def get_receiver_emails_csv(file):
    receiver_emails = []
    with open(file, mode='r') as csv_file:
        key = Prompt.ask("Enter emails column title ")
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            receiver_emails.append(line[key])
        preprocess_emails(receiver_emails)
    return receiver_emails

def get_receiver_emails_file():
    receiver_emails = []
    SUPPORTED_EXTENTSION = ["txt","csv"]
    supported_files = [f for f in os.listdir() if f.split(".")[-1] in SUPPORTED_EXTENTSION]
    if len(supported_files) == 0:
        console.print(Panel(f'''[red]Sorry, There are not any Supported Files in Current Directory [/red]
We support {str(SUPPORTED_EXTENTSION)[1:-1]}.
If you need other types add an issue on Github: https://github.com/AhmedNasserG and we will add them ASAP
Please Add One And Try Again''', style="bold"))
        sys.exit()
    file = showMenu("Select Email Body File :", supported_files)
    if file.split(".")[-1] == "txt":
        get_receiver_emails_txt(file)
    elif file.split(".")[-1] == "csv":
        get_receiver_emails_csv(file)
    return receiver_emails

def get_receiver_emails():
    mod = Prompt.ask("Way of Entering Receiver E-mails :", choices=["manual", "file"], default="manual")
    if mod == "manual":
        receiver_emails = get_receiver_emails_manual()
    elif mod == "file":
        receiver_emails = get_receiver_emails_file()
    return receiver_emails

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
# receiver_emails, email = get_receiver_emails(), get_mail_content()
# send_mail(receiver_emails, email)
# print("done")
# get_mail_content()
# get_receiver_emails_manual()
get_receiver_emails()
# print(show_checklist("test", ["op1","op2","op3","op4"]))