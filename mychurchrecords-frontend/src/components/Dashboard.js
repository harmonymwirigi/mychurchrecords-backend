import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function DashboardComponent() {
    const [attendanceData, setAttendanceData] = useState([]);
    const [donationData, setDonationData] = useState([]);
    const [formData, setFormData] = useState({
        member_id: '',
        meeting_date: '',
        amount: '',
        donation_date: ''
    });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    // Fetch attendance and donation records
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            navigate('/');  // Redirect to login if no token
        } else {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;  // Attach token for authenticated requests

            const fetchAttendance = async () => {
                try {
                    const response = await axios.get('http://localhost:5000/api/attendance');
                    setAttendanceData(response.data);
                } catch (error) {
                    console.error('Error fetching attendance data', error);
                }
            };

            const fetchDonations = async () => {
                try {
                    const response = await axios.get('http://localhost:5000/api/donations');
                    setDonationData(response.data);
                } catch (error) {
                    console.error('Error fetching donation data', error);
                }
            };

            fetchAttendance();
            fetchDonations();
        }
    }, [navigate]);

    // Handle form input
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    // Handle attendance submission
    const handleAttendanceSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:5000/api/attendance', {
                member_id: formData.member_id,
                meeting_date: formData.meeting_date
            });
            alert('Attendance record added successfully');
            setFormData({ ...formData, meeting_date: '' });  // Clear form
        } catch (error) {
            setError('Error adding attendance record');
        }
    };

    // Handle donation submission
    const handleDonationSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:5000/api/donation', {
                member_id: formData.member_id,
                amount: formData.amount,
                date: formData.donation_date
            });
            alert('Donation record added successfully');
            setFormData({ ...formData, amount: '', donation_date: '' });  // Clear form
        } catch (error) {
            setError('Error adding donation record');
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Dashboard</h2>

            {/* Error Handling */}
            {error && <div className="alert alert-danger">{error}</div>}

            <div className="row">
                <div className="col-lg-6 mb-4">
                    {/* Form to Add Attendance */}
                    <div className="card">
                        <div className="card-header">
                            <h5>Add Attendance</h5>
                        </div>
                        <div className="card-body">
                            <form onSubmit={handleAttendanceSubmit}>
                                <div className="mb-3">
                                    <label className="form-label">Member ID</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        name="member_id"
                                        placeholder="Member ID"
                                        value={formData.member_id}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Meeting Date</label>
                                    <input
                                        type="date"
                                        className="form-control"
                                        name="meeting_date"
                                        value={formData.meeting_date}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-primary">Add Attendance</button>
                            </form>
                        </div>
                    </div>
                </div>

                <div className="col-lg-6 mb-4">
                    {/* Form to Add Donation */}
                    <div className="card">
                        <div className="card-header">
                            <h5>Add Donation</h5>
                        </div>
                        <div className="card-body">
                            <form onSubmit={handleDonationSubmit}>
                                <div className="mb-3">
                                    <label className="form-label">Member ID</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        name="member_id"
                                        placeholder="Member ID"
                                        value={formData.member_id}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Amount</label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        name="amount"
                                        placeholder="Amount"
                                        value={formData.amount}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Donation Date</label>
                                    <input
                                        type="date"
                                        className="form-control"
                                        name="donation_date"
                                        value={formData.donation_date}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-primary">Add Donation</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            {/* Display Attendance Records */}
            <h3 className="mt-4">Attendance Records</h3>
            <table className="table table-striped">
                <thead className="thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Member ID</th>
                        <th>Meeting Date</th>
                    </tr>
                </thead>
                <tbody>
                    {attendanceData.map((record) => (
                        <tr key={record.id}>
                            <td>{record.id}</td>
                            <td>{record.member_id}</td>
                            <td>{record.meeting_date}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Display Donation Records */}
            <h3 className="mt-4">Donation Records</h3>
            <table className="table table-striped">
                <thead className="thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Member ID</th>
                        <th>Amount</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {donationData.map((record) => (
                        <tr key={record.id}>
                            <td>{record.id}</td>
                            <td>{record.member_id}</td>
                            <td>{record.amount}</td>
                            <td>{record.date}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default DashboardComponent;
