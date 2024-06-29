import urllib.request
import smtplib
from email.message import EmailMessage
import threading
from getpass import getpass
import re

currentIP = ''
SMTP_Address = {
'gmail':"smtp.gmail.com",
'outlook':"smtp-mail.outlook.com",
'yahoo': "smtp.mail.yahoo.com"
 }
   
def createEmail(subject:str, message:str,fromEmail:str,toEmail:str) -> EmailMessage:
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = fromEmail
    msg['To'] = toEmail
    msg.set_content(message) 
    return msg


def sendEmail(emailMessage:EmailMessage,credentials):
    try:
        server = smtplib.SMTP(credentials["SMTP_Server"], 587)
        server.starttls()
        server.login(emailMessage['From'], credentials['password'])  # user & password
        server.send_message(emailMessage)
        server.quit()
        print('successfully sent the mail.')
    except Exception as e:
        print(e)     
        raise()
    
def monitorIP(credentials):
    global currentIP
    timer = None
    try:
        newIP = str(urllib.request.urlopen('https://ident.me').read().decode('utf8'))
        if(newIP == currentIP):
            print("IP has not changed")
            return
        print("IP has changed to " + newIP)
        fromEmail = credentials['fromEmail']
        emailMessage = createEmail("IP Changed", newIP, fromEmail, fromEmail)
        sendEmail(emailMessage, credentials)
        currentIP = newIP
        timer = threading.Timer(10, monitorIP, [credentials])
        timer.start()
            
    except Exception as e:
        print(e)
        if timer != None:
            timer.cancel()
        raise ValueError(e)


def getInputs() -> dict[str, str]:
    while True:
        try:
            fromEmail = input("Enter Email: ")
            if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', fromEmail):
                raise ValueError('Please enter a valid email')
            provider = fromEmail.split('@')[1].split('.')[0]
            SMTP_Server = SMTP_Address.get(provider)
            if not SMTP_Server:
                raise ValueError('Unsupported provider, please try another email')
            password = getpass('Password: ')
            return {"fromEmail": fromEmail, "password": password, "SMTP_Server": SMTP_Server}
        except ValueError as e:
            print(e)
        
def main():
    max_retries = 5
    attempts = 0
    while attempts < max_retries:
        try:
            credentials = getInputs()
            monitorIP(credentials)
            break
        except Exception as e:
            print(f"Error occurred: {e}. Retrying... ({attempts + 1}/{max_retries})")
            attempts += 1
            if attempts >= max_retries:
                print("Maximum retry limit reached. Exiting.")
                break

main()



