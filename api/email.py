import smtplib
from flask import current_app


def send_email(subject, recipients, msg):
    if current_app.config['TESTING']:
        return
    server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
    try:
        server.ehlo()
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
    except smtplib.SMTPNotSupportedError:
        print('SMTP does not support tls or login')
    payload = dict()
    payload['From'] = current_app.config['MAIL_SENDER']
    if isinstance(recipients, list):
        payload['To'] = ', '.join(recipients)
    else:
        payload['To'] = recipients
    payload['Subject'] = subject
    payload['msg'] = msg
    msg = "\r\n".join([
        "From: " + payload['From'],
        "To: " + payload['To'],
        "Subject: " + payload['Subject'],
        "",
        payload['msg']
    ])    
    server.sendmail(current_app.config['MAIL_SENDER'], recipients, msg)
    server.quit()
