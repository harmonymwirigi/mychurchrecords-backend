import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AdminTable from '../components/AdminTable';

const AdminDashboard = ({ type }) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('access_token');

        if (!token) {
            setError('You must be logged in to access this data.');
            setLoading(false);
            return;
        }

        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        // List of valid types
        const validTypes = ['churches', 'donations', 'meetings'];
        if (!validTypes.includes(type)) {
            setError('Invalid data type specified.');
            setLoading(false);
            return;
        }
        
        // Determine the correct endpoint based on the type
        let endpoint;
        switch (type) {
            case 'churches':
                endpoint = 'http://localhost:5000/api/admin/churches';
                break;
            case 'donations':
                endpoint = 'http://localhost:5000/api/admin/donations';
                break;
            case 'meetings':
                endpoint = 'http://localhost:5000/api/admin/meetings';
                break;
            default:
                // This should not be reached due to the check above
                setError('Invalid data type specified.');
                setLoading(false);
                return;
        }

        const fetchData = async () => {
            try {
                const response = await axios.get(endpoint);
                setData(response.data);
            } catch (error) {
                setError('Failed to fetch data from the server.');
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [type]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }

    return (
        <div>
            <h2>Admin Dashboard - {type.charAt(0).toUpperCase() + type.slice(1)}</h2>
            <AdminTable data={data} type={type} />
        </div>
    );
};

export default AdminDashboard;
