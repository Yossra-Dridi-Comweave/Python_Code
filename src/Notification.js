import React from 'react';
import './Notification.css'; // Assure-toi d'avoir un fichier CSS pour le style

function Notification({ message, type }) {
    if (!message) return null;

    return (
        <div className={`notification ${type}`}>
            {message}
        </div>
    );
}

export default Notification;
