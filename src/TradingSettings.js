import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Notification from './Notification'; // Importe le composant de notification
import './TradingSettings.css';
import { useLocation } from 'react-router-dom';

function TradingSettings() {
    const [symbols, setSymbols] = useState([]);
    const [selectedSymbol, setSelectedSymbol] = useState('');
    const [takeProfit, setTakeProfit] = useState(0);
    const [lotSize, setLotSize] = useState(0.0);
    const [stopLoss, setStopLoss] = useState(0);
    const [closeThreshold, setCloseThreshold] = useState(0);
    const [timeFrame, setTimeFrame] = useState('TIMEFRAME_M1');
    const [notification, setNotification] = useState({ message: '', type: '' });
    const location = useLocation(); // Accéder à l'objet location
    const query = new URLSearchParams(location.search);
    const loginSuccess = query.get('loginSuccess') === 'true'; // Vérifier si le paramètre loginSuccess est 'true'
    const [showLoginSuccess, setShowLoginSuccess] = useState(loginSuccess);
    useEffect(() => {
        if (loginSuccess) {
            const timer = setTimeout(() => {
                setShowLoginSuccess(false); // Cacher le message après 5000 millisecondes (5 secondes)
            }, 2000);

            return () => clearTimeout(timer); // Nettoyage du timer si le composant est démonté
        }
    }, [loginSuccess]);
    useEffect(() => {
        async function loadSymbols() {
            const response = await axios.get('http://localhost:5000/symbols');
            setSymbols(response.data.symbols);
            setSelectedSymbol(response.data.symbols[0]);
        }
        loadSymbols();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
    
        // Validation des entrées
        if (!selectedSymbol) {
            setNotification({ message: 'Please select a symbol.', type: 'error' });
            return;
        }
        if (isNaN(takeProfit) || takeProfit <= 0) {
            setNotification({ message: 'Take Profit must be a positive number.', type: 'error' });
            return;
        }
        if (isNaN(lotSize) || lotSize <= 0) {
            setNotification({ message: 'Lot Size must be a positive number.', type: 'error' });
            return;
        }
        if (isNaN(stopLoss) || stopLoss <= 0) {
            setNotification({ message: 'Stop Loss must be a positive number.', type: 'error' });
            return;
        }
       
        if (!timeFrame) {
            setNotification({ message: 'Please select a time frame.', type: 'error' });
            return;
        }
    
        // Si toutes les validations sont passées, effectuer la requête POST
        axios.post('http://localhost:5000/saveSettings', {
            symbol: selectedSymbol,
            takeProfit: parseFloat(takeProfit),
            lotSize: lotSize,
            timeFrame: timeFrame
        })
        .then(response => {
            setNotification({ message: 'Settings saved successfully!', type: 'success' });
        })
        .catch(error => {
            setNotification({ message: 'Error saving settings.', type: 'error' });
        });
       
    
        try {
            const response = await axios.post('http://127.0.0.1:5000/executeTrade');
            console.log(response.data.message);  // Afficher le message de succès ou d'erreur
            if (response.data.status === 'success') {
                alert('Trade executed successfully');
            } else {
                alert('Error executing trade');
            }
        } catch (error) {
            console.error('Error making the request:', error);
            alert('Network error or server is down');
        }
    };
    

    return (
        <div className="settings-container">
            {showLoginSuccess && (
                <Notification message="Login Successful!" type="success" />
            )}
            <h2>Trading Settings</h2>
            <form onSubmit={handleSubmit}>
            <label>
                    Symbol:
                    <select value={selectedSymbol} onChange={e => setSelectedSymbol(e.target.value)}>
                        {symbols.map(symbol => (
                            <option key={symbol} value={symbol}>{symbol}</option>
                        ))}
                    </select>
                </label>
                <label>
                    Lot Size:
                    <input type="float" value={lotSize} onChange={e => setLotSize(e.target.value)} />
                </label>
                <label>
                    Take Profit:
                    <input type="float" value={takeProfit} onChange={e => setTakeProfit(e.target.value)} />
                </label>
                <label>
                    Stop Loss:
                    <input type="float" value={stopLoss} onChange={e => setStopLoss(e.target.value)} />
                </label>
               
                <label>
                    Time Frame:
                    <select value={timeFrame} onChange={e => setTimeFrame(e.target.value)}>
                        <option value="TIMEFRAME_M1">M1</option>
                        <option value="TIMEFRAME_M5">M5</option>
                        <option value="TIMEFRAME_M15">M15</option>
                        <option value="TIMEFRAME_M30">M30</option>
                        <option value="TIMEFRAME_H1">H1</option>
                    </select>
                </label>
                <Notification message={notification.message} type={notification.type} />
                <button type="submit">Save Settings</button>
            </form>
        </div>
    );
}

export default TradingSettings;


