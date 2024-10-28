from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Church(db.Model):
    __tablename__ = 'church'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pastor_name = db.Column(db.String(100))
    location_city = db.Column(db.String(100))
    location_state = db.Column(db.String(100))
    location_country = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    subscription_start = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Password field
    
    # Relationships
    payments = db.relationship('Payment', backref='church', lazy='dynamic')
    donations = db.relationship('Donation', backref='church', lazy='dynamic')
    attendances = db.relationship('Attendance', backref='church', lazy='dynamic')
    members = db.relationship('ChurchMember', backref='church', lazy='dynamic')

    def __repr__(self):
        return f"<Church {self.name}>"

    # Method to set the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ChurchMember(db.Model):
    __tablename__ = 'church_member'
    
    id = db.Column(db.Integer, primary_key=True)
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'), nullable=False)
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

    def __repr__(self):
        return f"<ChurchMember {self.first_name} {self.last_name}>"


class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'), nullable=False)
    meeting_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Attendance {self.meeting_date} for Church ID {self.church_id}>"


class Donation(db.Model):
    __tablename__ = 'donation'
    
    id = db.Column(db.Integer, primary_key=True)
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Donation {self.amount} on {self.date} for Church ID {self.church_id}>"


class Payment(db.Model):
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payment {self.amount} on {self.payment_date} for Church ID {self.church_id}>"


class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f"<AdminUser {self.name}>"

    # Method to set the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
