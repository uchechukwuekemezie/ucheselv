from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from forms import SignUpForm, LoginForm, DashboardForm, LoanApplicationForm
from models import db, User, LoanApplication
import random

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
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        password = form.password.data

        users[email] = {'name': name, 'phone': phone, 'password': password}

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        email_phone = form.email_phone.data
        password = form.password.data

        # Check if user exists and password is correct 
        user = users.get(email_phone)
        if user and user['password'] == password:
            session['user_email'] = email_phone  
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

    form = DashboardForm(request.form)

    if request.method == 'POST' and form.validate():
        # Dashboard logic here
        return redirect(url_for('main.apply_loan'))

    return render_template('dashboard.html', form=form)

@main.route('/apply_loan', methods=['GET', 'POST'])
def apply_loan():
    if 'user_email' not in session:
        flash('Please log in to apply for a loan.', 'warning')
        return redirect(url_for('main.login'))

    form = LoanApplicationForm(request.form)

    if request.method == 'POST' and form.validate():
        # Loan application logic here
        return render_template('repayment_plan.html')

    return render_template('apply_loan.html', form=form)

# Add a route for logging out
@main.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
