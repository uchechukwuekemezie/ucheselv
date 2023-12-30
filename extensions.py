from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
# from app import mail

bcrypt = Bcrypt()
mail = Mail()

def send_loan_application_email(email, loan_application_id):
    msg = Message('Loan Application Submitted', recipients=[email])
    msg.body = f'Your loan application (ID: {loan_application_id}) has been submitted for processing.'
    mail.send(msg)