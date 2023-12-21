from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    email_phone = StringField('Email/Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class DashboardForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    bvn = StringField('BVN', validators=[DataRequired()])
    nin = StringField('NIN', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    employment_status = SelectField('Employment Status', choices=[('employed', 'Employed'), ('unemployed', 'Unemployed')],
                                    validators=[DataRequired()])
    marital_status = SelectField('Marital Status', choices=[('single', 'Single'), ('married', 'Married')],
                                 validators=[DataRequired()])


class LoanApplicationForm(FlaskForm):
    purpose = StringField('Purpose for Loan', validators=[DataRequired()])
    business_name = StringField('Name of Business', validators=[DataRequired()])
    loan_amount = DecimalField('Loan Amount', validators=[DataRequired()])
    tenure = StringField('Tenure (Months)', validators=[DataRequired()])

# additional features - may be removed

class WalletFundingForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired()])
    submit = SubmitField('Fund Wallet')