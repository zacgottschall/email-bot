import imaplib
import email
from .outgoing_email import OutgoingEmail
from .incoming_email import IncomingEmail
from email.header import decode_header
from dateutil.parser import parse
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl


class EmailClient:
    def __init__(self, username: str, password: str):
        self.username: str = username
        self.password: str = password

    def get_new_emails(self):
        most_recent_timestamp = 0
        for From, subject, timestamp in self._read_emails():
            most_recent_timestamp = max(timestamp, most_recent_timestamp)

            last_check = get_last_check()
            if last_check is None:
                most_recent_timestamp = timestamp
                break

            if timestamp == get_last_check():
                break

            yield IncomingEmail(From, subject, timestamp)

        if most_recent_timestamp > 0:
            set_last_check(most_recent_timestamp)

    def send(self, outgoing_email: OutgoingEmail, recipient: str):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.username
        message["To"] = recipient
        message["Subject"] = outgoing_email.subject

        # Add body to email
        message.attach(MIMEText(outgoing_email.body, "plain"))

        if outgoing_email.filename is not None:
            # Open file in binary mode
            with open(outgoing_email.filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {outgoing_email.filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)

        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, recipient, text)

    def _read_emails(self):
        # create an IMAP4 class with SSL
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        imap.login(self.username, self.password)

        status, messages = imap.select("INBOX")

        num_messages = int(messages[0])

        i = num_messages
        while i > 0:
            try:
                res, msg = imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode()
                        # decode email sender
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        timestamp = parse(msg["Date"]).timestamp()
                        yield From, subject, timestamp
                i -= 1
            except:
                break


def get_last_check():
    with open('last_check', "r") as f:
        last_check = f.read()
        if last_check == '':
            return None
        return float(last_check)


def set_last_check(last_check):
    with open('last_check', "w") as f:
        return f.write(str(int(last_check)))

