from os import getenv, remove
from time import sleep
from email_bot.utils import process_incoming_email
from email_bot.models import IncomingEmail, EmailClient, OutgoingEmail
from email_bot.exceptions import TaskException


if __name__ == "__main__":
    username: str = getenv('EMAIL_BOT_USERNAME')
    password: str = getenv('EMAIL_BOT_PASSWORD')

    email_client = EmailClient(username, password)

    incoming_email: IncomingEmail

    while True:
        for incoming_email in email_client.get_new_emails():
            try:
                outgoing_email: OutgoingEmail = process_incoming_email(incoming_email)
                email_client.send(outgoing_email, incoming_email.frm)
                remove(outgoing_email.filename)
            except TaskException as e:
                email_client.send(OutgoingEmail(
                    subject="Something went wrong",
                    body="Contact zacharygottschall@gmail.com",
                ), incoming_email.frm)
                email_client.send(OutgoingEmail(
                    subject="Email Bot Error",
                    body="Input: {}\nError: {}".format(incoming_email.frm, str(e))
                ), 'zacharygottschall@gmail.com')
        
        sleep(10)
