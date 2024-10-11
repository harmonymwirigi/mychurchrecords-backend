// mychurchrecords-frontend/src/components/ChurchList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function ChurchList() {
    const [churchData, setChurchData] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            navigate('/');  // Redirect to login if no token
        } else {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;  // Attach token for authenticated requests

            const fetchChurches = async () => {
                try {
                    const response = await axios.get('http://localhost:5000/api/admin/churches');
                    setChurchData(response.data);
                } catch (error) {
                    setError('Error fetching church data');
                    console.error('Error fetching church data:', error);
                }
            };

            fetchChurches();
        }
    }, [navigate]);

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }

    return (
        <div className="container mt-4">
            <h3 className="mb-4">Church List</h3>
            {churchData.length === 0 ? (
                <p>No churches available.</p>
            ) : (
                <table className="table table-striped">
                    <thead className="thead-dark">
                        <tr>
                            <th>Name</th>
                            <th>Pastor Name</th>
                            <th>City</th>
                            <th>State</th>
                            <th>Country</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Verified</th>
                        </tr>
                    </thead>
                    <tbody>
                        {churchData.map((church) => (
                            <tr key={church.id}>
                                <td>{church.name}</td>
                                <td>{church.pastor_name}</td>
                                <td>{church.location_city}</td>
                                <td>{church.location_state}</td>
                                <td>{church.location_country}</td>
                                <td>{church.email}</td>
                                <td>{church.phone}</td>
                                <td>{church.is_verified ? 'Yes' : 'No'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default ChurchList;
