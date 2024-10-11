import React, { useState } from 'react';
import axios from 'axios';

function ChurchFormComponent() {
    const [formData, setFormData] = useState({
        name: '',
        pastor_name: '',
        location_city: '',
        location_state: '',
        location_country: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: ''  // New field for confirming password
    });

    const [passwordError, setPasswordError] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Check if passwords match
        if (formData.password !== formData.confirmPassword) {
            setPasswordError("Passwords do not match!");
            return;  // Stop form submission
        }

        try {
            const response = await axios.post('http://localhost:5000/api/churches', formData);
            alert('Church created successfully!');
        } catch (error) {
            console.error('There was an error creating the church!', error);
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Create New Church</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="name" className="form-label">Church Name</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        id="name" 
                        name="name" 
                        placeholder="Enter church name"
                        value={formData.name} 
                        onChange={handleChange}
                        required 
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="pastor_name" className="form-label">Pastor Name</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        id="pastor_name" 
                        name="pastor_name" 
                        placeholder="Enter pastor's name"
                        value={formData.pastor_name} 
                        onChange={handleChange}
                        required 
                    />
                </div>
                <div className="row">
                    <div className="col-md-4 mb-3">
                        <label htmlFor="location_city" className="form-label">City</label>
                        <input 
                            type="text" 
                            className="form-control" 
                            id="location_city" 
                            name="location_city" 
                            placeholder="City"
                            value={formData.location_city} 
                            onChange={handleChange}
                            required 
                        />
                    </div>
                    <div className="col-md-4 mb-3">
                        <label htmlFor="location_state" className="form-label">State</label>
                        <input 
                            type="text" 
                            className="form-control" 
                            id="location_state" 
                            name="location_state" 
                            placeholder="State"
                            value={formData.location_state} 
                            onChange={handleChange}
                            required 
                        />
                    </div>
                    <div className="col-md-4 mb-3">
                        <label htmlFor="location_country" className="form-label">Country</label>
                        <input 
                            type="text" 
                            className="form-control" 
                            id="location_country" 
                            name="location_country" 
                            placeholder="Country"
                            value={formData.location_country} 
                            onChange={handleChange}
                            required 
                        />
                    </div>
                </div>
                
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
                    <label htmlFor="phone" className="form-label">Phone</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        id="phone" 
                        name="phone" 
                        placeholder="Enter phone number"
                        value={formData.phone} 
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
                <div className="mb-3">
                    <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                    <input 
                        type="password" 
                        className="form-control" 
                        id="confirmPassword" 
                        name="confirmPassword" 
                        placeholder="Confirm your password"
                        value={formData.confirmPassword} 
                        onChange={handleChange}
                        required 
                    />
                </div>

                {passwordError && <p className="text-danger">{passwordError}</p>}

                <button type="submit" className="btn btn-primary">Create Church</button>
            </form>
        </div>
    );
}

export default ChurchFormComponent;
