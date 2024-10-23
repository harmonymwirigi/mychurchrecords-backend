import React from 'react';
import { useNavigate } from 'react-router-dom';

function LogoutButton() {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Remove token from local storage
        localStorage.removeItem('access_token');
        
        // Redirect to the login page
        navigate('/');
    };

    return (
        <button onClick={handleLogout} className="btn btn-danger">
            Logout
        </button>
    );
}

export default LogoutButton;
