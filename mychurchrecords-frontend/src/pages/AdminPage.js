// mychurchrecords-frontend/src/pages/AdminDashboard.js
import React from 'react';
import DonationList from '../components/DonationList';
import ChurchList from '../components/ChurchList';
import MeetingList from '../components/MeetingList';

const AdminDashboard = () => {
    return (
        <div className="container mt-4">
            <h2>Admin Dashboard</h2>
            <div className="mb-4">
                <ChurchList />
            </div>
            <div className="mb-4">
                <DonationList />
            </div>
            <div className="mb-4">
                <MeetingList />
            </div>
        </div>
    );
};

export default AdminDashboard;
