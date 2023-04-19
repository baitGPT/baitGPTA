""" Fetch emails from public email adress,
download attachments to a folder"""


#Receive :
import imaplib
import email
#Send :
import smtplib
from email.message import EmailMessage
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
#Usual utilities
import re
import os
import json



def clean(file_name):
    # clean file_name for saving purposes
    def cln(txt):
        return "".join(c if c.isalnum() else "_" for c in txt)
    print(file_name)
    if file_name[-4]=='.':#file.xyz
        return cln(file_name[:-4])+file_name[-4:]
    if file_name[-3]=='.':#file.yz
        return cln(file_name[:-3])+file_name[-3:]


def download_to_folder(username, password, imap_server, folder, verbose = True):
    """download all the attachment emails from the inbox, and put the mails as read"""
    conn = imaplib.IMAP4_SSL(imap_server)
    try:
        (retcode, capabilities) = conn.login(username, password)
    except:
        print(sys.exc_info()[1])
        sys.exit(1)
    conn.select(readonly=True)
    (retcode, messages) = conn.search(None, '(UNSEEN)') #Get unseen messages
    messages_list = []
    if retcode == 'OK':
        for num in messages[0].split():
            typ, data = conn.fetch(num,'(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            typ, data = conn.store(num,'-FLAGS','\\Seen')
            num_emails = 0
            for part in msg.walk():
                if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):
                    filename, encoding = decode_header(part.get_filename())[0]
                    if encoding:
                        save_path = os.path.join(folder,clean(filename.decode(encoding)))
                    else :
                        save_path = os.path.join(folder,clean(filename))
                    if os.path.isfile(save_path):
                        print(save_path)
                        () #We already have an email with the same Subject
                    elif save_path.endswith('eml'):  #only saving emails
                        with open(save_path, "w") as text_file:
                            print(type(part.get_payload(decode=True)))
                            print(type('\n'.join(part.as_string(part.get_payload(decode=True)).split('\n')[6:])))
                            text_file.write('\n'.join(part.as_string(part.get_payload(decode=True)).split('\n')[6:]))
                        num_emails+=1
            print(f"{num_emails} email{('s' if num_emails>1 else '')} downloaded")
    conn.close()
    return ()
if __name__ == "__main__": #for testing purposes
    # Open the JSON file
    with open('credential_head.json', 'r') as f:
        # Load the JSON data into a dictionary -> list of users
        users = json.load(f)["users"]
    # account credentials
    username = users[0]["email"]
    password = users[0]["password"]
    imap_server  = users[0]["imap_server"]
    smtp_server = users[0]["smtp_server"]
    smtp_port = users[0]["smtp_port"]
    folder = '/received'
    download_to_folder(username, password, imap_server, folder)
    ()
