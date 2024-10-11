// mychurchrecords-frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard'; // Example page
import Subscribe from './pages/Subscribe';
import ProtectedRoute from './components/ProtectedRoute';
import AdminPage from './pages/AdminPage'; // Example page
import LoginForm from './components/LoginForm';
import SubscriptionPage from './pages/SubscriptionPage'; // Example page
import AdminDashboard from './pages/AdminDashboard'; // Import AdminDashboard

function App() {
    return (
        <Router>
            <Routes>
                <Route
                    path="/admin"
                    element={
                        <ProtectedRoute allowedRoles={['admin']}>
                            <AdminDashboard />
                        </ProtectedRoute>
                    }
                />
                <Route path="/" element={<Subscribe />} />
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />
                <Route path="/admin-page" element={<AdminPage />} />
                <Route path="/login" element={<LoginForm />} />
                <Route path="/subscription" element={<SubscriptionPage />} />
            </Routes>
        </Router>
    );
}

export default App;
