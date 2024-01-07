from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms import DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import FloatField, validators


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])


class LoginForm(FlaskForm):
    email_phone = StringField('Email/Phone Number',
                              validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])


class DashboardForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    bvn = StringField('BVN', validators=[DataRequired()])
    nin = StringField('NIN', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    employment_status = SelectField(
        'Employment Status',
        choices=[('employed', 'Employed'), ('unemployed', 'Unemployed')],
        validators=[DataRequired()]
    )
    marital_status = SelectField(
        'Marital Status',
        choices=[('single', 'Single'), ('married', 'Married')],
        validators=[DataRequired()]
    )


class LoanApplicationForm(FlaskForm):
    purpose = StringField('Purpose for Loan', validators=[DataRequired()])
    business_name = StringField('Name of Business',
                                validators=[DataRequired()])
    loan_amount = DecimalField('Loan Amount', validators=[DataRequired()])
    tenure = StringField('Tenure (Months)', validators=[DataRequired()])
    submit = SubmitField('Apply')


# additional features - may be removed

class WalletFundingForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired()])
    submit = SubmitField('Fund Wallet')


class DocumentUploadForm(FlaskForm):
    document = FileField('Upload Document', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDFs only!')
    ])
    submit = SubmitField('Upload')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset Password')


class SavingsApplicationForm(FlaskForm):
    savings_type_choices = [
        ('Regular Savings Accounts', 'Regular Savings Accounts'),
        ('High-Yield Savings Plans', 'High-Yield Savings Plans'),
        ('Targeted Savings Accounts', 'Targeted Savings Accounts')
    ]

    payment_method_choices = [
        ('Cash', 'Cash'),
        ('Bank Deposit', 'Bank Deposit'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Direct Account Debit', 'Direct Account Debit'),
        ('Payment from Wallet', 'Payment from Wallet')
    ]

    savings_type = SelectField(
        'Savings Type',
        choices=savings_type_choices,
        validators=[validators.InputRequired()]
    )

    initial_payment_amount = FloatField(
        'Initial Payment Amount',
        validators=[validators.InputRequired()]
    )

    savings_frequency = SelectField(
        'Savings Frequency',
        choices=[('Monthly', 'Monthly'), ('Quarterly',
                                          'Quarterly'), ('Yearly', 'Yearly')],
        validators=[validators.InputRequired()]
    )

    method_of_payment = SelectField(
        'Method of Payment',
        choices=payment_method_choices,
        validators=[validators.InputRequired()]
    )

    submit = SubmitField('Submit Application')
