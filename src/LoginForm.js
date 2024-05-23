import React, { useState } from 'react';
import axios from 'axios';
import './LoginForm.css';
import { useHistory } from 'react-router-dom';

function LoginForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [server, setServer] = useState('IC_Markets');
    const history = useHistory();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/login', {
                username,
                password,
                server
            });
            if (response.data.status === "success") {
                history.push('/settings'); // Redirige vers la page des paramètres de trading
            } else {
                alert(response.data.message);
            }
        } catch (error) {
            console.error('Login failed:', error);
            alert('Login failed: ' + error.message);
        }
    };

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
                        <option value="IC_Markets">IC Markets</option>
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
