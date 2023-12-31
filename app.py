from flask import Flask
from routes import main
from models import db, User, LoanApplication
#from flask_bcrypt import Bcrypt
from extensions import bcrypt, mail
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from forms import ResetPasswordRequestForm, ResetPasswordForm
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from flask_mail import Mail, Message
from forms import SignUpForm, LoginForm, DashboardForm, LoanApplicationForm, WalletFundingForm, DashboardForm


# from flask import Flask
# from models import db
# from extensions import bcrypt, mail
# from flask_login import LoginManager

app = Flask(__name__)

#@app.before_first_request
def create_admin():
    if not User.query.filter_by(email="amadasunese@gmail.com").first():
        hashed_password = hash_password('1234567')
        admin_user = User(name="Admin", email="amadasunese@gmail.com", password=hashed_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"


# app.secret_key = 'assessment development'

# Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'amadasunese@gmail.com'
app.config["MAIL_PASSWORD"] = 'qxxo axga dzia jjsw'
mail = Mail(app)



s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def send_password_reset_email(user):
    token = s.dumps(user.email, salt='password-reset-salt')
    msg = Message('Reset Your Password', sender='amadasunese@gmail.com', recipients=[user.email])
    msg.body = f"To reset your password, visit the following link: {url_for('main.reset_password', token=token, _external=True)}"
    mail.send(msg)


@main.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('If your email is in our system, you will receive a password reset email shortly.')
        return redirect(url_for('main.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('reset_password_request'))

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('reset_password_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Update user's password
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('main.login'))
    return render_template('reset_password.html', title='Reset Password', form=form, token=token)


@main.route('/apply_loan', methods=['GET', 'POST'])
def apply_loan():
    if 'user_email' not in session:
        flash('Please log in to apply for a loan.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(email=session['user_email']).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.login'))

    form = LoanApplicationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Create a new loan application instance
        loan_application = LoanApplication(
            user_id=user.id,
            purpose=form.purpose.data,
            business_name=form.business_name.data,
            loan_amount=form.loan_amount.data,
            tenure=form.tenure.data,
            status='Pending'  # Assuming you have a status field to track application status
            # Add any other fields as necessary
        )
        db.session.add(loan_application)
        db.session.commit()

        # Send email notification (optional)
        send_loan_application_email(user.email, loan_application.id)

        flash('Your loan application has been submitted and is being processed.', 'success')
        return redirect(url_for('main.dashboard'))  # Redirecting to dashboard where status can be viewed

    return render_template('apply_loan.html', form=form)

# def send_loan_application_email(email, loan_application_id):
#     msg = Message('Loan Application Submitted', recipients=[email])
#     msg.body = f'Your loan application (ID: {loan_application_id}) has been submitted and is being processed.'
#     mail.send(msg)

def send_loan_application_email(email, loan_application_id):
    msg = Message('Loan Application Submitted', 
                  sender='amadasunese@gmail.com',  # Add the sender here
                  recipients=[email])
    msg.body = f'Your loan application (ID: {loan_application_id}) has been submitted for processing.'
    mail.send(msg)

@app.route('/send_contact_email', methods=['POST'])
def send_contact_email():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    msg = Message("Contact Form Submission",
                  sender=email,
                  recipients=["amadasunese@gmail.com.com"])
    msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    mail.send(msg)
    flash('Your message has been sent. Thank you for contacting us!', 'success')
    return redirect(url_for('main.contact'))



db.init_app(app)
bcrypt.init_app(app)


# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


# # with app.app_context():
#     if not User.query.filter_by(email="amadasunese@gmail.com").first():
#         admin_user = User(
#             name="Admin",
#             email="amadasunese@gmail.com",
#             password=bcrypt.generate_password_hash('1234567').decode('utf-8'),
#             is_admin=True
#         )
#         db.session.add(admin_user)
#         db.session.commit()

app.register_blueprint(main)

# def send_loan_application_email(user, loan_application_id):
#     msg = Message('Loan Application Submitted', recipients=[user.email])
#     msg.body = f'Your loan application (ID: {loan_application_id}) has been submitted for processing.'
#     mail.send(msg)


# def send_password_reset_email(user):
#     token = s.dumps(user.email, salt='password-reset-salt')
#     msg = Message('Reset Your Password', sender='amadasunese@gmail.com', recipients=[user.email])
#     msg.body = f"To reset your password, visit the following link: {url_for('main.reset_password', token=token, _external=True)}"
#     mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
