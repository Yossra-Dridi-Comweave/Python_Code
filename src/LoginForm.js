import React, { useState } from 'react';
import axios from 'axios';
import './LoginForm.css'; // Assurez-vous que ce fichier existe et contient les styles nécessaires
import { Navigate } from 'react-router-dom';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

function LoginForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [server, setServer] = useState('ICMarketsSC-Demo');
    const [redirectToSettings, setRedirectToSettings] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [passwordShown, setPasswordShown] = useState(false); // État pour contrôler l'affichage du mot de passe
    const [error, setError] = useState('');

    const togglePasswordVisibility = () => {
        setPasswordShown(!passwordShown); // Basculer la visibilité du mot de passe
    };
   

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!username || !password) {
            setError("Les champs utilisateur et mot de passe sont obligatoires.");
            return;
        }
        if (!/^\d+$/.test(username)) {
            setError("Le login doit être un nombre.");
            return;
        }

        setIsLoading(true);
        try {
            const response = await axios.post('http://localhost:5000/login', {
                username,
                password,
                server
            });
            if (response.data.status === "success") {
                setTimeout(() => {
                    setRedirectToSettings(true);
                    
                    localStorage.setItem('token', response.data.token);
                }, 2000);
            } else {
                setError(response.data.message);
            }
        } catch (e) {
            setError("Une erreur est survenue lors de la connexion.");
        }
        setIsLoading(false);
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
                    <input
                        type="text"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        placeholder="Enter username"
                    />
                </div>
                <div className="form-group">
                    <label>Mot de passe:</label>
                    <div className="password-field">
                        <input
                            type={passwordShown ? "text" : "password"}
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            placeholder="Enter password"
                        />
                        <button
                            type="button"
                            onClick={togglePasswordVisibility}
                            className="password-toggle"
                        >
                            <FontAwesomeIcon icon={passwordShown ? faEyeSlash : faEye} />
                        </button>
                    </div>
                </div>
                <div className="form-group">
                    <label>Serveur:</label>
                    <select value={server} onChange={e => setServer(e.target.value)}>
                        <option value="ICMarketsSC-Demo">ICMarketsSC-Demo</option>
                        <option value="MetaQuotes-Demo">MetaQuotes-Demo</option>
                        <option value="Admirals">Admirals</option>
                    </select>
                </div>
                {error && <div className="error">{error}</div>}
                <button
                    className="submit-button"
                    type="submit"
                    disabled={isLoading}
                >
                    {isLoading ? 'Connexion en cours...' : 'Connexion'}
                </button>
            </form>
        </div>
    );
}

export default LoginForm;
