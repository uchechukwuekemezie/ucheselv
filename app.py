#!/usr/bin/env python3
"""
Loans and Savings web application
"""
from flask import Flask
from routes import main
from models import db, User
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from forms import ResetPasswordRequestForm, ResetPasswordForm
from flask import render_template
from flask import redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"


# Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'amadasunese@gmail.com'
app.config["MAIL_PASSWORD"] = 'qxxo axga dzia jjsw'
mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def send_password_reset_email(user):
    """Password reset email
    """
    token = s.dumps(user.email, salt='password-reset-salt')
    msg = Message('Reset Your Password', sender='amadasunese@gmail.com',
                  recipients=[user.email])
    msg.body = (
        f"To reset your password, visit the following link: "
        f"{url_for('main.reset_password', token=token, _external=True)}"
    )
    mail.send(msg)


@main.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Process password reset request
    """
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Password reset email sent if your email is in our system.')
        return redirect(url_for('main.login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
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
    return render_template('reset_password.html',
                           title='Reset Password', form=form, token=token)


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


app.register_blueprint(main)


if __name__ == '__main__':
    app.run(debug=True)
