import smtplib
import json
import os
import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
            log.writeLogFile(
                'mail', 'info', '### Try connecting to server ###')
            # Try to log to the mail server
            s.login(MY_ADRESS, PASSWD)
            log.writeLogFile(
                'mail', 'info', 'Identification success')
        except smtplib.SMTPAuthenticationError:
            log.writeLogFile(
                'mail', 'info', 'FAILED: Server retuned bad username or password')
            break
        except smtplib.SMTPException:
            log.writeLogFile(
                'mail', 'info', 'FAILED: SERVER ABOUT TO DESTROY HUMANITY')
            break

        message = "The message to put in the mail"
        # Send the mail or not obviously
        if not s.sendmail(MY_ADRESS, CONTACT_ADRESS, message):
            log.writeLogFile('mail', 'info', 'The mail has been sent')
        else:
            log.writeLogFile('mail', 'critical', 'Failed to send mail')
        s.quit()
