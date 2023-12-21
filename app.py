from flask import Flask
from routes import main
from models import db
#from flask_bcrypt import Bcrypt
from extensions import bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"

db.init_app(app)
bcrypt.init_app(app)

# # Set up the login manager
# login_manager = LoginManager()
# login_manager.init_app(app)


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
