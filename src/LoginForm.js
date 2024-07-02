import React, { useState } from 'react';
import axios from 'axios';
import './LoginForm.css';
import { Navigate } from 'react-router-dom';

function LoginForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [server, setServer] = useState('ICMarketsSC-Demo');
    const [redirectToSettings, setRedirectToSettings] = useState(false);
    const [loginSuccess, setLoginSuccess] = useState(false); // État pour gérer l'affichage du message

    const handleSubmit = async (event) => {
        event.preventDefault();
        const response = await axios.post('http://localhost:5000/login', {
            username,
            password,
            server
        });
        if (response.data.status === "success") {
            setLoginSuccess(true); // Mettre à jour l'état pour afficher le message de succès
            setTimeout(() => { // Utiliser setTimeout pour retarder la redirection
                setRedirectToSettings(true);
            }, 2000); // Retarder de 2000 millisecondes (2 secondes)
        } else {
            alert(response.data.message);
        }
    };

    if (redirectToSettings) {
        return <Navigate to="/settings?loginSuccess=true" replace />;
    }
    return (
        <div className="login-container">
            <h2>Connexion Trader</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Login:</label>
                    <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
                </div>
                <div className="form-group">
                    <label>Mot de passe:</label>
                    <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </div>
                <div className="form-group">
                    <label>Serveur:</label>
                    <select value={server} onChange={e => setServer(e.target.value)}>
                        <option value="ICMarketsSC-Demo">ICMarketsSC-Demo</option>
                        <option value="MetaQuotes-Demo">MetaQuotes-Demo</option>
                        <option value="Admirals">Admirals</option>
                    </select>
                </div>
                <button type="submit">Connexion</button>
                
            </form>
        </div>
    );
}

export default LoginForm;
