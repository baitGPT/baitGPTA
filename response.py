#Receive :
import imaplib
import email
#Send :
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
from head_server import download_to_folder
#Usual utilities
import re
import os
import json
from utilities import body_from_email
from time import sleep
#GPT:
import openai

def talk(messages_history, question, Verbose=True, timing=False, max_tokens = 300, temperature=0): #parameters to investiguate
  answer = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= messages_history+[{"role": "user", "content": question}], max_tokens=max_tokens, temperature=temperature)
  text_answer = answer["choices"][0]["message"]["content"]
  if Verbose :
      print("GPT : " + text_answer)
  return messages_history+[{"role": "user", "content": question}, answer["choices"][0]["message"]]

def response(txt): #Generate a response to a scam email
    placeholder = "This is a placeholder email.\n With kind regards. \n\n\n Eric"
    Discussion = [{"role": "system", "content": "You are a helpful assistant in providing automated answers to scam emails."}]
    first_question = "Here is a message I received :\n"+txt+"\n(End of the message)\n\nIs this email a potential scam? Answer only with YES or NO. In case of huge uncertainty or insuficent informations, answer DOUBT."
    #Short answer, fully deterministic :
    Discussion = talk(Discussion, first_question, Verbose=True, timing=False, max_tokens = 5, temperature=0)
    patternNo = re.compile("\s*(N|n)(O|o)")
    patternYes = re.compile("\s*(Y|y)(E|e)(S|s)")
    if patternNo.match(Discussion[-1]["content"]):
        raise Exception("Not a spam"+txt)
    elif patternYes.match(Discussion[-1]["content"]):
        #We want to generate an automated answers
        second_question = "Please generate an answer to this scam email, which aims at not answering directly the email, but to request further details,or to pretend misunderstanding something and requesting other guidances. You can play dumb and put some humour. Work around giving any complete personal informations.\n It should be in the same language as the initial email, not too long, and should'nt contain strong language.\nIf the senders name isn't explicit, use 'J. D.' as signature of the email.\nJust answer with the body of the email."
        #Longer answer, with more randomness for originality
        Discussion = talk(Discussion, second_question, Verbose=True, timing=False, max_tokens = 300, temperature=1.2)
        return Discussion[-1]["content"]
    else :
        raise Exception(f"Parsing Error on string '{Discussion[-1]['content']}', Doesn't match YES OR NO")

def RE(original,smtp_server, smtp_port, username, password, safeguard = True): #Send the response to the sender
    #Create the text part of the message :
    #Txt = response + f" \n On {msg.date_str}, {msg.from_values.name if msg.from_values else msg.from_} wrote : \n" + (msg.html if msg.html else msg.txt)
    #connect to the server
    new = MIMEMultipart("mixed")
    new["Message-ID"] = email.utils.make_msgid()
    new["In-Reply-To"] = original["Message-ID"]
    new["References"] = original["Message-ID"]
    new["Subject"] = "Re: "+original["Subject"]
    new["To"] = original["Reply-To"] or original["From"]
    new["From"] = username
    original_text = body_from_email(original)
    with open("received_body.txt", "w") as text_file:
        text_file.write(original_text)
    #print(original_text)
    Date_line = f"On {original['Date']}, <{original['Reply-To'] or original['From']}> wrote:"
    try:
        body = MIMEText(response(original_text)+"\n\n" + Date_line)
    except Exception:
        print(f"Not A Spam ({original['Subject']})")
        return ()
    new.attach(body)
    new.attach(MIMEText(original_text))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    newstr=new.as_string()
    #print(newstr)
    with open("Output.txt", "w") as text_file:
        text_file.write(newstr)
    if safeguard and input("Send  to {new['To']} ?(y/n)")=='y':
        return()
    else :
        #server.sendmail(username, [new["To"]], newstr) #Uncomment to launch
        server.quit()
        print(f"Email sent to {new['To']}!")
        if not safeguard :
            sleep(50)
