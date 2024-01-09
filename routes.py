from flask import Blueprint, render_template, request
from flask import request, redirect, url_for, session, flash, abort
from forms import SignUpForm, LoginForm, DashboardForm, LoanApplicationForm
from forms import WalletFundingForm, DashboardForm
from models import db, User, LoanApplication, SavingsApplication
import random
from forms import WalletFundingForm, DocumentUploadForm
from flask_login import current_user
from flask_login import login_required
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash


main = Blueprint('main', __name__)

mail = Mail()

# Dummy data for user storage
users = {}


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)

    if request.method == 'POST' and form.validate():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.signup'))

        # Hash password before storing
        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password
        )
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('main.login'))
    except Exception:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')

    return render_template('signup.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email_phone.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # Set user details in session
            session['user_email'] = user.email
            session['user_name'] = user.name

            # Check if the user is an admin
            if user.is_admin:
                session['is_admin'] = True
                flash('Admin login successful', 'success')
                return redirect(url_for('main.admin_dashboard'))
            else:
                session['is_admin'] = False
                flash('Login successful', 'success')

            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html', form=form)


@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(email=session['user_email']).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.login'))

    form = DashboardForm(obj=user)  # Pre-populate form with user data

    if request.method == 'POST' and form.validate():
        # Update user details
        user.name = form.name.data
        user.address = form.address.data
        user.bvn = form.bvn.data
        user.nin = form.nin.data
        user.dob = form.dob.data
        user.employment_status = form.employment_status.data
        user.marital_status = form.marital_status.data

        # Generate a random 10-digit account number if not already present
        if not user.account_number:
            user.account_number = ''.join(str(random.randint(0, 9))
                                          for _ in range(10))

        db.session.commit()

        flash('Your details have been updated.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('dashboard.html', form=form)


# Add a route for logging out
@main.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_name', None)  # Clearing user name from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))


@main.route('/fund_wallet', methods=['GET', 'POST'])
def fund_wallet():
    form = WalletFundingForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=session['user_email']).first()
        amount_to_add = form.amount.data

        payment_successful = process_payment(amount_to_add)

        if payment_successful:
            user = User.query.get(user_id)
            if user:
                user.wallet_balance += amount_to_add
                db.session.commit()
                flash('Wallet funded successfully!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('User not found.', 'error')
        else:
            flash('Payment failed. Please try again.', 'error')

    return render_template('fund_wallet.html', form=form)


@main.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    form = DocumentUploadForm()
    if form.validate_on_submit():
        # Save the document and update user's verification status
        pass
    return render_template('upload_document.html', form=form)


@main.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_email' not in session:
        flash('Please log in to update your profile.', 'warning')
        return redirect(url_for('main.login'))

    # user identification  done via email stored in session
    user = User.query.filter_by(email=session['user_email']).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = DashboardForm(obj=user)

    if request.method == 'POST' and form.validate_on_submit():
        # Update user details
        user.name = form.name.data
        user.address = form.address.data
        user.bvn = form.bvn.data
        user.nin = form.nin.data
        user.dob = form.dob.data
        user.employment_status = form.employment_status.data
        user.marital_status = form.marital_status.data
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('update_profile.html', form=form)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/calculator')
def calculator():
    return render_template('calculator.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/loans')
def loans():
    return render_template('loans.html')


@main.route('/faq')
def faq():
    return render_template('faq.html')


@main.route('/fixed-deposit')
def fixed_deposit():
    return render_template('fixed_deposit.html')


@main.route('/savings')
def savings():
    return render_template('savings.html')


@main.route('/invest')
def invest():
    return render_template('invest.html')


@main.route('/savings_plan')
def savings_plan():
    return render_template('savings_plan.html')


@main.route('/admin_dashboard')
# @login_required
def admin_dashboard():
        return render_template('admin_dashboard.html')


@main.route('/admin_users')
# @login_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)


@main.route('/admin_loan_applications')
# @login_required
def admin_loan_applications():
    loan_applications = LoanApplication.query.all()  # Fetch all loan applications
    return render_template('admin_loan_applications.html', loan_applications=loan_applications)


@main.route('/admin_savings_applications')
# @login_required
def admin_savings_applications():
    # SavingsApplication model
    savings_applications = SavingsApplication
    return render_template('admin_savings_applications.html',
                           savings_applications=savings_applications)


@main.route('/savings_application', methods=['GET', 'POST'])
def savings_application():
    if 'user_email' not in session:
        flash('Please log in to apply for a loan.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(email=session['user_email']).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        savings_type = request.form['savings_type']
        initial_payment_amount = float(request.form['initial_payment_amount'])
        savings_frequency = request.form['savings_frequency']
        method_of_payment = request.form.getlist('method_of_payment')
        # Extract other form fields as needed

        application = SavingsApplication(
            savings_type=savings_type,
            initial_payment_amount=initial_payment_amount,
            savings_frequency=savings_frequency,
            method_of_payment=', '.join(method_of_payment)
            # Assign other fields here
        )

        db.session.add(application)
        db.session.commit()

        return redirect(url_for('main.view_savings_applications'))

    return render_template('savings_application_form.html')


@main.route('/view_savings_applications')
def view_savings_applications():
    applications = SavingsApplication.query.all()
    return render_template('view_savings_applications.html',
                           applications=applications)


@main.route('/bills-payment')
def bills_payment():

    return render_template('bills_payment.html')


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
            status='Pending'
        )
        db.session.add(loan_application)
        db.session.commit()

        # Send email notification (optional)
        send_loan_application_email(user.email, loan_application.id)

        flash('Your loan application has been submitted.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('apply_loan.html', form=form)


def send_loan_application_email(email, loan_application_id):
    msg = Message('Loan Application Submitted',
                  sender='amadasunese@gmail.com',
                  recipients=[email])
    msg.body = (
        f'Your loan application with (ID number: {loan_application_id}) '
        'has been submitted for processing.'
    )

    mail.send(msg)


@main.route('/send_contact_email', methods=['POST'])
def send_contact_email():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    msg = Message("Contact Form Submission",
                  sender=email,
                  recipients=["amadasunese@gmail.com.com"])
    msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    mail.send(msg)
    flash('Your message has been sent.', 'success')
    return redirect(url_for('main.contact'))


@main.route('/delete_user/<int:user_id>')
# @login_required  
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User successfully removed', 'success')
    else:
        flash('User not found', 'error')
    return redirect(url_for('main.admin_dashboard'))  
