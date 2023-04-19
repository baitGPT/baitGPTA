#Receive :
import imaplib
import email
#Usual utilities
import re
import os
import json
import html2text
#GPT:

def text_from_html(txt):
    h = html2text.HTML2Text()
    # Ignore converting links from HTML
    h.ignore_links = False
    return h.handle(txt)

def email_from_folder(path, verbose = True):
    Msg=[]
    for file in os.listdir(path):
        if file.endswith('.eml'):
            with open(os.path.join(path,file), 'rb') as fp:
                msg = email.message_from_bytes(fp.read())
                Msg.append(msg) #we should remove the attachements
        elif verbose:
            print(f"{file} isn't an email")
    print(f"{len(Msg)} email{('s' if len(Msg)>1 else '')} retrieved from {path}.")
    return Msg
def body_from_email(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload()  # decode
                break
    else:
        if msg.get_content_type() == 'text/plain':
            body = msg.get_payload()
        elif msg.get_content_type() == 'text/html':
            body = text_from_html(msg.get_payload())
        else:
            raise Exception(f"Unknown content type : {msg.get_content_type()}")
    pattern = re.compile("\s*$")
    body = '\n'.join([x for x in re.split('\n|\|', body) if (not pattern.match(x))]) #single \n and no |

    return body


def read_last_email2(username, password, imap_server):
    conn = imaplib.IMAP4_SSL(imap_server)
    try:
        (retcode, capabilities) = conn.login(username, password)
    except:
        #print(sys.exc_info()[1])
        sys.exit(1)
    conn.select(readonly=True) # Select inbox or default namespace
    (retcode, messages) = conn.search(None, '(UNSEEN)') #Get unseen messages
    messages_list = []
    if retcode == 'OK':
        for num in messages[0].split():
            typ, data = conn.fetch(num,'(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            typ, data = conn.store(num,'-FLAGS','\\Seen')
            messages_list.append(msg)
            for part in msg.walk(): #remove attachement
                #if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                #print(20*"="+"PART"+20*"=")
                #print(part)
                #print(20*"="+"PARTEND"+20*"=")
                if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):
                    del part["Content-Disposition"]
                    del part["Content-Transfer-Encoding"]
    conn.close()
    return messages_list
