import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function DonationList() {
    const [donationData, setDonationData] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    // Fetch donation records
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            navigate('/');  // Redirect to login if no token
        } else {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;  // Attach token for authenticated requests

            const fetchDonations = async () => {
                try {
                    const response = await axios.get('http://localhost:5000/api/admin/donations');
                    setDonationData(response.data);
                } catch (error) {
                    setError('Error fetching donation data');
                    console.error('Error fetching donation data:', error);
                }
            };

            fetchDonations();
        }
    }, [navigate]);

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }

    return (
        <div className="container mt-4">
            <h3 className="mb-4">Donation Records</h3>
            {donationData.length === 0 ? (
                <p>No donations available.</p>
            ) : (
                <table className="table table-striped">
                    <thead className="thead-dark">
                        <tr>
                            <th>ID</th>
                            <th>Church ID</th>
                            <th>Church Name</th> {/* Optionally display church name */}
                            <th>Amount</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {donationData.map((record) => (
                            <tr key={record.id}>
                                <td>{record.id}</td>
                                <td>{record.church_id}</td>
                                <td>{record.church_name}</td> {/* Optionally display church name */}
                                <td>{record.amount}</td>
                                <td>{record.date}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default DonationList;
