from awd_main.celery import app
from dataentry.utils import *


@app.task
def send_email_task(mail_subject,message, to_email,attachment):
    send_email_notification(mail_subject,message, to_email,attachment)
    return 'Email sending task executed succesfully'