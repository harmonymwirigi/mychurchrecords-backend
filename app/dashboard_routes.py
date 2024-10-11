from flask import Blueprint, request, jsonify
from app import db
from app.models import Attendance, Donation
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

# Add attendance record
@dashboard.route('/api/attendance', methods=['POST'])
def add_attendance():
    data = request.json
    member_id = data.get('member_id')
    meeting_date = data.get('meeting_date')
    
    if not member_id or not meeting_date:
        return jsonify({"error": "Member ID and meeting date are required"}), 400
    
    try:
        meeting_date = datetime.strptime(meeting_date, '%Y-%m-%d').date()
        attendance = Attendance(member_id=member_id, meeting_date=meeting_date)
        db.session.add(attendance)
        db.session.commit()
        return jsonify({"message": "Attendance record added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all attendance records
@dashboard.route('/api/attendance', methods=['GET'])
def get_attendance():
    attendance_records = Attendance.query.all()
    result = [
        {
            "id": attendance.id,
            "member_id": attendance.member_id,
            "meeting_date": attendance.meeting_date.strftime('%Y-%m-%d')
        } for attendance in attendance_records
    ]
    return jsonify(result), 200

# Add donation record
@dashboard.route('/api/donation', methods=['POST'])
def add_donation():
    data = request.json
    member_id = data.get('member_id')
    amount = data.get('amount')
    date = data.get('date')
    
    if not member_id or not amount or not date:
        return jsonify({"error": "Member ID, amount, and date are required"}), 400
    
    try:
        donation_date = datetime.strptime(date, '%Y-%m-%d').date()
        donation = Donation(member_id=member_id, amount=amount, date=donation_date)
        db.session.add(donation)
        db.session.commit()
        return jsonify({"message": "Donation record added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all donation records
@dashboard.route('/api/donations', methods=['GET'])
def get_donations():
    donation_records = Donation.query.all()
    result = [
        {
            "id": donation.id,
            "member_id": donation.member_id,
            "amount": donation.amount,
            "date": donation.date.strftime('%Y-%m-%d')
        } for donation in donation_records
    ]
    return jsonify(result), 200
