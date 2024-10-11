from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Church(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pastor_name = db.Column(db.String(100))
    location_city = db.Column(db.String(100))
    location_state = db.Column(db.String(100))
    location_country = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    subscription_start = db.Column(db.DateTime)
    is_verified = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Password field
    payments = db.relationship('Payment', backref='church', lazy=True)

    # Method to set the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    
class ChurchMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    dob = db.Column(db.Date)
    first_time_at_church = db.Column(db.Date)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('church_member.id'), nullable=False)
    meeting_date = db.Column(db.Date)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('church_member.id'), nullable=False)
    date = db.Column(db.Date)
    amount = db.Column(db.Float)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'), nullable=False)
    amount = db.Column(db.Float)
    payment_date = db.Column(db.DateTime)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.String(20))
