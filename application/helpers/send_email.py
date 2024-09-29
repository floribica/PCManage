import os
import smtplib

from dotenv import load_dotenv
from flask import render_template

load_dotenv()
ADMINEMAIL = os.getenv("ADMINEMAIL")
PASSWORD = os.getenv("PASSWORD")
COMPANY_NAME = os.getenv("COMPANY_NAME")


def send_email(to_addr, subject, html_content):
    sender = f"{COMPANY_NAME} <{ADMINEMAIL}>"
    msg = f"From: {sender}\r\nTo: {to_addr}\r\nSubject: {
        subject}\r\nContent-Type: text/html\r\n\r\n{html_content}"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(ADMINEMAIL, PASSWORD)
    server.sendmail(sender, to_addr, msg)
    server.quit()


def password_email(username, password):
    return render_template(
        'emails/create_account.html',
        username=username,
        password=password
    )


def password_email(username, password):
    return render_template(
        'emails/reset_password.html',
        username=username,
        password=password
   )
