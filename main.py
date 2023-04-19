#Receive :
import imaplib
import email
#Send :
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
#local functions
from head_server import download_to_folder
from utilities import email_from_folder, read_last_email2
from response import RE
#Usual utilities
import re
import os
import json
import random
#GPT:
import openai

def main(safeguard=True):
    # Open the JSON files
    with open('GPTkey.json', 'r') as f:
        # Get the api_key
        openai.api_key = json.load(f)["api_key"]
    #Gathering email adress
    with open('credential.json', 'r') as f:
        # Load the JSON data into a dictionary -> list of users
        h_users = json.load(f)["users"]
    head_user= h_users[0]
    #Senders email adresses
    with open('credential.json', 'r') as f:
        # Load the JSON data into a dictionary -> list of users
        users = json.load(f)["users"]
    #### Head Server downloads all the gathered emails:
    download_to_folder(head_user["email"], head_user["password"], head_user["imap_server"],"received/")
    messages_list= email_from_folder("received")
    for msg in messages_list:
        #Pick a sender
        i=random.randint(0,len(users)-1)
        username = users[i]["email"]
        password = users[i]["password"]
        smtp_server = users[i]["smtp_server"]
        smtp_port = users[i]["smtp_port"]
        #Generate and send a response
        RE(msg,smtp_server, smtp_port, username, password, safeguard)
    ### autoresponses in mailboxes
    for user in users:
        break
        username = user["email"]
        password = user["password"]
        imap_server  = user["imap_server"]
        smtp_server = user["smtp_server"]
        smtp_port = user["smtp_port"]
        messages_list = read_last_email2(username, password, imap_server)
        for msg in messages_list[-1:]:
            RE(msg,smtp_server, smtp_port, username, password, safeguard)
if __name__ == "__main__":
    main()
    #email_from_folder("received")
    #msg = read_last_email2(username, password, imap_server)
    #with open("received.txt", "w") as text_file:
    #    text_file.write(msg.as_string())
    #RE(msg)
