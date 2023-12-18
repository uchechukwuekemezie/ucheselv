from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(10), unique=True)
    address = db.Column(db.String(255))
    bvn = db.Column(db.String(11))
    nin = db.Column(db.String(11))
    dob = db.Column(db.Date)
    employment_status = db.Column(db.String(10))
    marital_status = db.Column(db.String(10))


class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purpose = db.Column(db.String(255), nullable=False)
    business_name = db.Column(db.String(255), nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    tenure = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

