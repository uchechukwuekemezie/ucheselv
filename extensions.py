#!/usr/bin/env python3
"""
Extension for sending loan application
through email
"""
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

bcrypt = Bcrypt()
mail = Mail()


def send_loan_application_email(email, loan_application_id):
    """Send loan application through email
    """
    msg = Message('Loan Application Submitted', recipients=[email])
    msg.body = f'Your loan application (ID: {loan_application_id}) ' \
        f'has been submitted for processing.'
    mail.send(msg)
