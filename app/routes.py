from flask import Blueprint, request, jsonify, url_for
from .models import db, Church, AdminUser, Donation, Attendance,ChurchMember
from datetime import datetime
from flask_mail import Message
from . import mail
import requests
import os
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask import redirect
from flask import request, jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import create_access_token, JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))

PAYPAL_API_URL = "https://api.sandbox.paypal.com"  # Use the sandbox URL for testing

# Function to create a PayPal order
def create_paypal_order():
    # Step 1: Get PayPal access token
    client_id = os.getenv('PAYPAL_CLIENT_ID')
    secret = os.getenv('PAYPAL_SECRET')

    auth_response = requests.post(
        f"{PAYPAL_API_URL}/v1/oauth2/token",
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        data={"grant_type": "client_credentials"},
        auth=(client_id, secret)
    )

    if auth_response.status_code != 200:
        raise Exception("Failed to authenticate with PayPal")

    access_token = auth_response.json()['access_token']

    # Step 2: Create a PayPal order
    order_response = requests.post(
        f"{PAYPAL_API_URL}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": "20.00"
                    }
                }
            ]
        }
    )

    if order_response.status_code != 201:
        raise Exception("Failed to create PayPal order")

    order_data = order_response.json()

    # Get approval URL to redirect user to PayPal
    for link in order_data['links']:
        if link['rel'] == 'approve':
            return link['href']

    raise Exception("No approval link found in PayPal order response")

def create_admin_user(name, email, password, phone):
    # Check if an admin already exists
    existing_admin = AdminUser.query.first()
    if existing_admin:
        print("An admin user already exists. Only one admin user is allowed.")
        return

    # Create new admin user
    admin = AdminUser(
        name=name,
        email=email,
        password=generate_password_hash(password),  # Ensure password is hashed
        phone=phone
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully.")
    
@main.route('/api/churches', methods=['POST'])
def create_church():
    data = request.json
    subscription_start = datetime.utcnow()
    
    # Ensure 'password' is provided in the request data
    if 'password' not in data:
        return jsonify({"error": "Password is required."}), 400
    
    # Hash the password before storing it
    hashed_password = generate_password_hash(data['password'])

    new_church = Church(
        name=data['name'],
        pastor_name=data['pastor_name'],
        location_city=data['location_city'],
        location_state=data['location_state'],
        location_country=data['location_country'],
        email=data['email'],
        phone=data['phone'],
        subscription_start=subscription_start,
        is_verified=False,
        password_hash=hashed_password  # Store hashed password
    )

    try:
        db.session.add(new_church)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback the transaction if any error occurs
        return jsonify({"error": str(e)}), 500

    # Generate a secure token for email verification
    token = generate_verification_token(new_church.email)
    verification_url = url_for('main.verify_email', token=token, _external=True)
    send_verification_email(new_church.email, verification_url)

    return jsonify({"message": "Church registered! Please verify your email."}), 201


def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email


# Email verification route
@main.route('/api/verify_email/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
        # send a notification to admin@churchrecords.us
    except:
        return jsonify({"error": "Invalid or expired token."}), 400

    church = Church.query.filter_by(email=email).first_or_404()

    if church.is_verified:
        return jsonify({"message": "Email already verified. Proceed to payment."}), 200

    # Mark the church as verified
    church.is_verified = True
    db.session.commit()

    # Create a PayPal order for $20
    try:
        paypal_approval_url = create_paypal_order()  # Create the PayPal order
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Redirect the user to PayPal for payment
    return redirect(paypal_approval_url)

# Send verification email
def send_verification_email(to_email, verification_url):
    msg = Message('Verify your email', sender=os.getenv('MAIL_USERNAME'), recipients=[to_email])
    msg.body = f'Please click the link to verify your email: {verification_url}'
    mail.send(msg)
client_id = os.getenv('PAYPAL_CLIENT_ID')

print(client_id)
# PayPal payment (mock example)
@main.route('/api/paypal_checkout', methods=['POST'])
def paypal_checkout():
    # PayPal payment setup
    paypal_api = "https://api.sandbox.paypal.com/v1/oauth2/token"
    client_id = os.getenv('PAYPAL_CLIENT_ID')
    secret = os.getenv('PAYPAL_SECRET')

    auth = (client_id, secret)
    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(paypal_api, headers=headers, auth=auth, data=data)

    if response.status_code == 200:
        token = response.json()['access_token']
        # Here you would create the PayPal order and redirect to PayPal's checkout URL
        # (This is a mock response for illustration purposes)
        return jsonify({"message": "Proceed to PayPal checkout", "paypal_token": token})
    else:
        return jsonify({"error": "Failed to authenticate PayPal."}), 500
    

@main.route('/api/login', methods=['POST'])
def login():
    data = request.json

    # Check if both email and password are provided in the request
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data['email']
    password = data['password']

    # Find user by email (check AdminUser first, then Church)
    user = AdminUser.query.filter_by(email=email).first()
    user_type = 'admin'

    if not user:
        user = Church.query.filter_by(email=email).first()
        user_type = 'church'

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Check if the provided password matches the hashed password in the database
    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate a JWT token with just the email
    access_token = create_access_token(identity=user.email)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user_type": user_type  # Return the user type
    }), 200

@main.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Get user data from the request
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    # Check if email already exists
    existing_admin = AdminUser.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({"error": "Email already registered."}), 400

    # Create a new AdminUser instance
    new_admin = AdminUser(
        name=name,
        email=email,
        phone=phone
    )
    new_admin.set_password(password)  # Hash the password

    # Add the new admin to the database
    try:
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({"message": "Admin user created successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create admin user."}), 500




# You can similarly define routes for members, attendance, donations, and admin functionality

@main.route('/api/members', methods=['POST'])
@jwt_required()
def create_member():
    data = request.json

    # Retrieve the logged-in church's identity
    church_email = get_jwt_identity()
    church = Church.query.filter_by(email=church_email).first()

    if not church:
        return jsonify({"error": "Church not found"}), 404

    # Extract member data from the request
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    dob = data.get('dob')
    first_time_at_church = data.get('first_time_at_church')

    # Check for required fields
    if not first_name or not last_name:
        return jsonify({"error": "First and last name are required"}), 400

    # Create new ChurchMember record
    try:
        member = ChurchMember(
            church_id=church.id,
            first_name=first_name,
            last_name=last_name,
            nickname=data.get('nickname'),
            email=email,
            phone=phone,
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            country=data.get('country'),
            dob=datetime.strptime(dob, '%Y-%m-%d').date() if dob else None,
            first_time_at_church=datetime.strptime(first_time_at_church, '%Y-%m-%d').date() if first_time_at_church else None
        )

        db.session.add(member)
        db.session.commit()

        return jsonify({"message": "Member added successfully", "member_id": member.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/api/members', methods=['GET'])
@jwt_required()
def get_members():
    # Retrieve the logged-in church's identity
    church_email = get_jwt_identity()
    church = Church.query.filter_by(email=church_email).first()

    if not church:
        return jsonify({"error": "Church not found"}), 404

    # Get all members associated with the logged-in church
    members = ChurchMember.query.filter_by(church_id=church.id).all()

    result = [{
        "id": member.id,
        "first_name": member.first_name,
        "last_name": member.last_name,
        "nickname": member.nickname,
        "email": member.email,
        "phone": member.phone,
        "address": member.address,
        "city": member.city,
        "state": member.state,
        "country": member.country,
        "dob": member.dob.strftime('%Y-%m-%d') if member.dob else None,
        "first_time_at_church": member.first_time_at_church.strftime('%Y-%m-%d') if member.first_time_at_church else None
    } for member in members]

    return jsonify(result), 200

@main.route('/api/admin/churches', methods=['GET'])
@jwt_required()
def get_all_churches():
    churches = Church.query.all()
    church_list = [{
        "id": church.id,
        "name": church.name,
        "pastor_name": church.pastor_name,
        "location_city": church.location_city,
        "location_state": church.location_state,
        "location_country": church.location_country,
        "email": church.email,
        "phone": church.phone,
        "is_verified": church.is_verified,
        "subscription_start": church.subscription_start
    } for church in churches]
    return jsonify(church_list), 200

@main.route('/api/admin/donations', methods=['GET'])
def get_all_donations():
    donations = Donation.query.all()
    donation_list = [{
        "id": donation.id,
        "church_id": donation.church_id,  # Correct reference to church_id
        "church_name": donation.church.name,  # Access the related church's name
        "date": donation.date.strftime('%Y-%m-%d'),
        "amount": donation.amount
    } for donation in donations]
    return jsonify(donation_list), 200

@main.route('/api/admin/meetings', methods=['GET'])
def get_all_meetings():
    meetings = Attendance.query.all()
    meeting_list = [{
        "id": meeting.id,
        "church_id": meeting.church_id,  # Now correctly references church_id
        "church_name": meeting.church.name,  # Access the related church's name
        "meeting_date": meeting.meeting_date.strftime('%Y-%m-%d')
    } for meeting in meetings]
    return jsonify(meeting_list), 200


