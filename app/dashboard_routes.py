from flask import Blueprint, request, jsonify
from app import db
from app.models import Attendance, Donation, Church
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard = Blueprint('dashboard', __name__)

# Add attendance record for logged-in church
@dashboard.route('/api/attendance', methods=['POST'])
@jwt_required()
def add_attendance():
    data = request.json
    meeting_date = data.get('meeting_date')
    
    if not meeting_date:
        return jsonify({"error": "Meeting date is required"}), 400
    
    try:
        # Retrieve logged-in church identity
        church_email = get_jwt_identity()
        church = Church.query.filter_by(email=church_email).first()
        
        if not church:
            return jsonify({"error": "Church not found"}), 404

        # Convert meeting_date to datetime object
        meeting_date = datetime.strptime(meeting_date, '%Y-%m-%d').date()
        
        # Create and add new attendance record
        attendance = Attendance(church_id=church.id, meeting_date=meeting_date)
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({"message": "Attendance record added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get attendance records for the logged-in church
@dashboard.route('/api/attendance', methods=['GET'])
@jwt_required()
def get_attendance():
    # Get the logged-in church's email from the JWT token
    church_email = get_jwt_identity()
    
    # Retrieve the church by email
    church = Church.query.filter_by(email=church_email).first()
    
    if not church:
        return jsonify({"error": "Church not found"}), 404
    
    # Get all attendance records for the logged-in church
    attendance_records = Attendance.query.filter_by(church_id=church.id).all()
    
    result = [
        {
            "id": attendance.id,
            "meeting_date": attendance.meeting_date.strftime('%Y-%m-%d')
        } for attendance in attendance_records
    ]
    
    return jsonify(result), 200

# Add donation record for logged-in church
@dashboard.route('/api/donation', methods=['POST'])
@jwt_required()
def add_donation():
    data = request.json
    amount = data.get('amount')
    date = data.get('date')
    
    if not amount or not date:
        return jsonify({"error": "Amount and date are required"}), 400
    
    try:
        # Retrieve logged-in church identity
        church_email = get_jwt_identity()
        church = Church.query.filter_by(email=church_email).first()
        
        if not church:
            return jsonify({"error": "Church not found"}), 404

        # Convert date to datetime object
        donation_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        # Create and add new donation record
        donation = Donation(church_id=church.id, amount=amount, date=donation_date)
        db.session.add(donation)
        db.session.commit()
        
        return jsonify({"message": "Donation record added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get donation records for the logged-in church
@dashboard.route('/api/donations', methods=['GET'])
@jwt_required()
def get_donations():
    # Get the logged-in church's email from the JWT token
    church_email = get_jwt_identity()
    
    # Retrieve the church by email
    church = Church.query.filter_by(email=church_email).first()
    
    if not church:
        return jsonify({"error": "Church not found"}), 404
    
    # Get all donation records for the logged-in church
    donation_records = Donation.query.filter_by(church_id=church.id).all()
    
    result = [
        {
            "id": donation.id,
            "amount": donation.amount,
            "date": donation.date.strftime('%Y-%m-%d')
        } for donation in donation_records
    ]
    
    return jsonify(result), 200