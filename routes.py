from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from forms import SignUpForm, LoginForm, DashboardForm, LoanApplicationForm, WalletFundingForm, DashboardForm
from models import db, User, LoanApplication
import random
from forms import WalletFundingForm, DocumentUploadForm
from extensions import bcrypt, mail
from flask_login import current_user
from flask_login import login_required
from forms import ResetPasswordRequestForm, ResetPasswordForm
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message


main = Blueprint('main', __name__)

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

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
    except:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')

    return render_template('signup.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email_phone.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Set user details in session
            session['user_email'] = user.email
            session['user_name'] = user.name
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
            user.account_number = ''.join(str(random.randint(0, 9)) for _ in range(10))

        db.session.commit()

        flash('Your details have been updated.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('dashboard.html', form=form)


#Add a route for logging out
@main.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_name', None)  # Clearing user name from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

# additional features

@main.route('/fund_wallet', methods=['GET', 'POST'])
@login_required
def fund_wallet():
    form = WalletFundingForm()
    if form.validate_on_submit():
        user_id = current_user.id  
        amount_to_add = form.amount.data

        payment_successful = process_payment(amount_to_add)

        if payment_successful:
            user = User.query.get(user_id)
            if user:
                user.wallet_balance += amount_to_add
                db.session.commit()
                flash('Wallet funded successfully!', 'success')
                return redirect(url_for('some_success_page'))
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

    #user identification  done via email stored in session
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

@main.route('/bills-payment')
def bills_payment():
    return render_template('bills_payment.html')

@main.route('/faq')
def faq():
    return render_template('faq.html')

@main.route('/fixed-deposit')
def fixed_deposit():
    return render_template('fixed_deposit.html')

@main.route('/savings')
def savings():
    return render_template('savings.html')

@main.route('/savings_plan')
def savings_plan():
    return render_template('savings_plan.html')

@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    # Additional logic if necessary
    return render_template('admin_dashboard.html')

@main.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@main.route('/admin/loan-applications')
@login_required
def admin_loan_applications():
    if not current_user.is_admin:
        abort(403)
    loan_applications = LoanApplication.query.filter_by(approval_status='pending').all()
    return render_template('admin_loan_applications.html', loan_applications=loan_applications)

@main.route('/admin/savings-applications')
@login_required
def admin_savings_applications():
    if not current_user.is_admin:
        abort(403)
    # SavingsApplication model
    savings_applications = SavingsApplication.query.filter_by(approval_status='pending').all()
    return render_template('admin_savings_applications.html', savings_applications=savings_applications)
