from flask import Flask
from routes import main
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key"

db.init_app(app)


with app.app_context():
    db.create_all()

app.register_blueprint(main)


if __name__ == '__main__':
    app.run(debug=True)
