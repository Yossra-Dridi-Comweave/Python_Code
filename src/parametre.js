import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TradingSettings() {
    const [symbols, setSymbols] = useState([]);
    const [selectedSymbol, setSelectedSymbol] = useState('');
    const [takeProfit, setTakeProfit] = useState(0);
    const [closeThreshold, setCloseThreshold] = useState(0);
    const [timeFrame, setTimeFrame] = useState('');

    // Chargement initial des symboles
    useEffect(() => {
        async function loadSymbols() {
            const response = await axios.get('http://localhost:5000/symbols');
            setSymbols(response.data.symbols);
            setSelectedSymbol(response.data.symbols[0]);
        }
        loadSymbols();
    }, []);

    return (
        <div>
            <h2>Trading Settings</h2>
            <form>
                <label>
                    Symbol:
                    <select value={selectedSymbol} onChange={e => setSelectedSymbol(e.target.value)}>
                        {symbols.map(symbol => (
                            <option key={symbol} value={symbol}>{symbol}</option>
                        ))}
                    </select>
                </label>
                <label>
                    Take Profit:
                    <input type="number" value={takeProfit} onChange={e => setTakeProfit(e.target.value)} />
                </label>
                <label>
                    Close Threshold:
                    <input type="number" value={closeThreshold} onChange={e => setCloseThreshold(e.target.value)} />
                </label>
                <label>
                    Time Frame:
                    <select value={timeFrame} onChange={e => setTimeFrame(e.target.value)}>
                        <option value="M1">M1</option>
                        <option value="M5">M5</option>
                        <option value="M15">M15</option>
                        <option value="M30">M30</option>
                        <option value="H1">H1</option>
                    </select>
                </label>
                <button type="submit">Save Settings</button>
            </form>
        </div>
    );
}

export default TradingSettings;
