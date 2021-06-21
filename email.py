from flask.ext.mail import Message

from project import app, mail


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender="sportseventer@gmail.com"
    )
    mail.send(msg)
