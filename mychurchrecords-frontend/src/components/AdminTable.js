import React from 'react';

const AdminTable = ({ data, type }) => {
    console.log('Data received:', data);
    console.log('Type:', type);

    if (!data || !data.length) {
        return <p>No data available</p>;
    }

    // Render table headers and rows based on data type
    const renderTableHeader = () => {
        switch (type) {
            case 'churches':
                return (
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
                );
            case 'donations':
                return (
                    <tr>
                        <th>ID</th>
                        <th>Church ID</th>
                        <th>Church Name</th> {/* Optionally add church name */}
                        <th>Date</th>
                        <th>Amount</th>
                    </tr>
                );
            case 'meetings':
                return (
                    <tr>
                        <th>ID</th>
                        <th>Church ID</th>
                        <th>Church Name</th> {/* Optionally add church name */}
                        <th>Meeting Date</th>
                    </tr>
                );
            default:
                return null;
        }
    };

    const renderTableRows = () => {
        return data.map((item, index) => {
            switch (type) {
                case 'churches':
                    return (
                        <tr key={index}>
                            <td>{item.name}</td>
                            <td>{item.pastor_name}</td>
                            <td>{item.location_city}</td>
                            <td>{item.location_state}</td>
                            <td>{item.location_country}</td>
                            <td>{item.email}</td>
                            <td>{item.phone}</td>
                            <td>{item.is_verified ? 'Yes' : 'No'}</td>
                        </tr>
                    );
                case 'donations':
                    return (
                        <tr key={index}>
                            <td>{item.id}</td>
                            <td>{item.church_id}</td>
                            <td>{item.church_name}</td> {/* Add church name if available */}
                            <td>{item.date}</td>
                            <td>{item.amount}</td>
                        </tr>
                    );
                case 'meetings':
                    return (
                        <tr key={index}>
                            <td>{item.id}</td>
                            <td>{item.church_id}</td>
                            <td>{item.church_name}</td> {/* Add church name if available */}
                            <td>{item.meeting_date}</td>
                        </tr>
                    );
                default:
                    return null;
            }
        });
    };

    return (
        <table>
            <thead>{renderTableHeader()}</thead>
            <tbody>{renderTableRows()}</tbody>
        </table>
    );
};

export default AdminTable;
