import smtplib
import json
import os
from email.mime.text import MIMEText as text
from src.log import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
Function to send mail
message = the message you want to send
subject = the subject of your message
config is loaded from a JSON. (will change in futur)
'''


def sendMail(message, subject):

    print(message)

    # Load the mail server configuration ( user mailconfig.json template )
    with open(BASE_DIR + '/config/mailconfig.json') as config_json:
        config = json.load(config_json)

        HOST = config['mail']['HOST']
        MY_ADRESS = config['mail']['USER']
        PASSWD = config['mail']['PASSWD']
        PORT = config['mail']['PORT']

# Load contact list ( use contact.json template )
    with open(BASE_DIR + '/config/contact.json') as contact_json:
        contacts = json.load(contact_json)
        for contact in contacts:
            CONTACT_NAME = contacts[contact]['NAME']
            CONTACT_ADRESS = contacts[contact]['ADRESS']

        # Add server info and start SSL/TLS
            s = smtplib.SMTP(host=HOST, port=PORT)
            s.starttls()

            try:
                # Try to log to the mail server
                s.login(MY_ADRESS, PASSWD)
            except smtplib.SMTPAuthenticationError:
                writeLogFile(
                    'mail', 'critical', 'FAILED: Server retuned bad username or password')
                break
            except smtplib.SMTPException:
                writeLogFile(
                    'mail', 'critical', 'FAILED: SERVER ABOUT TO DESTROY HUMANITY')
                break

            # Let's configure the mail
            message_to_send = text(message)
            message_to_send['From'] = MY_ADRESS
            message_to_send['To'] = CONTACT_ADRESS
            message_to_send['Subject'] = subject

            # Send the mail or not obviously
            if not s.sendmail(MY_ADRESS, CONTACT_ADRESS, message_to_send.as_string()):
                writeLogFile('mail', 'info', 'The mail has been sent')
            else:
                print('An error occured. Check log !')
            s.quit()
