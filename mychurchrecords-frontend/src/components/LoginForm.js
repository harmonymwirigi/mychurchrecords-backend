import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function LoginForm() {
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await axios.post('http://localhost:5000/api/login', formData);

            // Save access token and user type to local storage
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('user_type', response.data.user_type); // Save user type

            // Redirect based on user type
            if (response.data.user_type === 'admin') {
                navigate('/admin-page');
            } else {
                navigate('/dashboard');
            }

        } catch (error) {
            setLoading(false);
            setError(error.response?.data?.error || 'There was an error logging in.');
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input 
                        type="email" 
                        className="form-control" 
                        id="email" 
                        name="email" 
                        placeholder="Enter email"
                        value={formData.email} 
                        onChange={handleChange}
                        required 
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input 
                        type="password" 
                        className="form-control" 
                        id="password" 
                        name="password" 
                        placeholder="Enter your password"
                        value={formData.password} 
                        onChange={handleChange}
                        required 
                    />
                </div>

                {error && <p className="text-danger">{error}</p>}

                <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </form>
        </div>
    );
}

export default LoginForm;
