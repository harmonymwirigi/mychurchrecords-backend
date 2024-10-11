// mychurchrecords-frontend/src/components/MeetingList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function MeetingList() {
    const [meetingData, setMeetingData] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            navigate('/');  // Redirect to login if no token
        } else {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;  // Attach token for authenticated requests

            const fetchMeetings = async () => {
                try {
                    const response = await axios.get('http://localhost:5000/api/admin/meetings');
                    setMeetingData(response.data);
                } catch (error) {
                    setError('Error fetching meeting data');
                    console.error('Error fetching meeting data:', error);
                }
            };

            fetchMeetings();
        }
    }, [navigate]);

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }

    return (
        <div className="container mt-4">
            <h3 className="mb-4">Meeting List</h3>
            {meetingData.length === 0 ? (
                <p>No meetings available.</p>
            ) : (
                <table className="table table-striped">
                    <thead className="thead-dark">
                        <tr>
                            <th>ID</th>
                            <th>Member ID</th>
                            <th>Meeting Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {meetingData.map((meeting) => (
                            <tr key={meeting.id}>
                                <td>{meeting.id}</td>
                                <td>{meeting.member_id}</td>
                                <td>{meeting.meeting_date}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default MeetingList;
