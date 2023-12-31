# init_db.py

from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="amadasunese@gmail.com").first():
        hashed_password = generate_password_hash('1234567')
        admin_user = User(name="Admin", email="amadasunese@gmail.com", password=hashed_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
