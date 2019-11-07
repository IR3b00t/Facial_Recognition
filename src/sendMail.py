import smtplib
import json
import os
import log.py

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(BASE_DIR + '/config/mailconfig.json') as config_json:
    config = json.load(config_json)

    HOST = config['mail']['HOST']
    MY_ADRESS = config['mail']['USER']
    PASSWD = config['mail']['PASSWD']
    PORT = config['mail']['PORT']

with open(BASE_DIR + '/config/contact.json') as contact_json:
    contacts = json.load(contact_json)
    for contact in contacts:
        CONTACT_NAME = contacts[contact]['NAME']
        CONTACT_ADRESS = contacts[contact]['ADRESS']
        s = smtplib.SMTP(host=HOST, port=PORT)
        s.starttls()
        s.login(MY_ADRESS, PASSWD)
        message = "The message to put in the mail"
        if not s.sendmail(MY_ADRESS, CONTACT_ADRESS, message):
            logger.info('Mail envoyer')
        else:
            logger.error('Erreur d\'envoi du mail')
        s.quit()
