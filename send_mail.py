import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def sendmail(users, subject, alert_msg):
    FROMADDR = 'oswaldoeliezer876@gmail.com'
    PASSWORD = os.getenv("EMAIL_PASS")

    TOADDR   = [users[0]]
    CCADDR   = users[1:]

    # Create message container - the correct MIME type is multipart/alternative.
    msg            = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = FROMADDR
    msg['To']      = ', '.join(TOADDR)
    msg['Cc']      = ', '.join(CCADDR)

    # Create the body of the message 
    text = alert_msg

    # Record the MIME types of both parts - text/plain and text/html.
    body = MIMEText(text, 'plain')

    # Attach parts into message container.
    msg.attach(body)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com',587)
    # s.set_debuglevel(1)
    # s.ehlo()
    s.starttls()
    s.login(FROMADDR, PASSWORD)
    s.sendmail(FROMADDR, TOADDR+CCADDR, msg.as_string())
    s.quit()
