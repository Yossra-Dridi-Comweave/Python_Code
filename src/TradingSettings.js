import './TradingSettings.css';
import React, { useState, useEffect, useRef} from 'react';
import Select from 'react-select';
import axios from 'axios';
import Notification from './Notification';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrashAlt, faPlusCircle, faCheckCircle, faTimesCircle  } from '@fortawesome/free-solid-svg-icons';
import { useLocation } from 'react-router-dom';


function TradingSettings() {
    const [showForm, setShowForm] = useState(false);
    const [tradingConfigurations, setTradingConfigurations] = useState([]);
    const formRef = useRef(null); 
    const location = useLocation();
    const [selectedSymbols, setSelectedSymbols] = useState([]);
    const [symbols, setSymbols] = useState([]);
    const [botStatuses, setBotStatuses] = useState([]);
    const [selectedSymbol, setSelectedSymbol] = useState('');
    const [takeProfit, setTakeProfit] = useState('');
    const [lotSize, setLotSize] = useState('');
    const [timeFrame, setTimeFrame] = useState('TIMEFRAME_M1');
    const [notification, setNotification] = useState({ message: '', type: '' });
    const [searchTerm, setSearchTerm] = useState('');
    // Pagination states
    
    const recordsPerPage=5;
    
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(5);
    const [totalItems, setTotalItems] = useState(5);

   
   
    const query = new URLSearchParams(location.search);
    const loginSuccess = query.get('loginSuccess') === 'true';
    const [showLoginSuccess, setShowLoginSuccess] = useState(loginSuccess);
    // useEffect(() => {
    //     const loadConfigurations = async () => {
    //         try {
    //             const response = await axios.get('http://localhost:7000/config', {
    //                 params: {
    //                     page: currentPage,
    //                     limit: itemsPerPage,
    //                 },
    //             });
    //             setTradingConfigurations(response.data.configurations);
    //             setTotalItems(response.data.totalCount); // Assuming your backend returns the total count
    //             setBotStatuses(response.data.configurations.map(() => false));
    //         } catch (error) {
    //             console.error('Failed to fetch configurations:', error);
    //         }
    //     };
    //     loadConfigurations();
    // }, [currentPage, itemsPerPage]);
   
    useEffect(() => {
        const loadConfigurations = async () => {
            try {
                const token = localStorage.getItem('token');  // Récupération du token depuis le localStorage

                // Vérification si le token existe
                if (!token) {
                    console.error('No token found');
                    return;
                }

                const response = await axios.get('http://localhost:7000/getSettings', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                setTradingConfigurations(response.data);
                setBotStatuses(response.data.map(() => false));
            } catch (error) {
                console.error('Failed to fetch configurations:', error);
            }
        };

        loadConfigurations();
    }, []);  // Le tableau des dépendances est vide, ce qui signifie que l'effet s'exécute une fois au chargement du composant


    useEffect(() => {
        if (loginSuccess) {
            const timer = setTimeout(() => {
                setShowLoginSuccess(false);
            }, 2000);
            return () => clearTimeout(timer);
        }
    }, [loginSuccess]);

    useEffect(() => {
        async function loadSymbols() {
            try {
                const response = await axios.get('http://localhost:5000/symbols');
                const options = response.data.symbols.map(symbol => ({ value: symbol, label: symbol }));
                setSymbols(options);
                if (options.length > 0) {
                    setSelectedSymbol(options[0]);
                }
            } catch (error) {
                console.error('Failed to fetch symbols:', error);
            }
        }
        loadSymbols();
    }, []);

    const onEditClick = async (id) => {
        const configToEdit = tradingConfigurations.find(config => config._id === id);
        if (configToEdit) {
            setSelectedSymbol({ value: configToEdit.symbol, label: configToEdit.symbol });
            setLotSize(configToEdit.lotSize.toString());
            setTakeProfit(configToEdit.takeProfit.toString());
            setTimeFrame(configToEdit.timeFrame);
            setShowForm(true);
        }
    };


    const onDeleteClick = async (id) => {
        try {
            await axios.delete(`http://localhost:7000/delete/${id}`);
            const updatedConfigurations = tradingConfigurations.filter(config => config._id !== id);
            setTradingConfigurations(updatedConfigurations);
            setNotification({ message: 'Configuration deleted successfully!', type: 'success' });
        } catch (error) {
            console.error('Failed to delete configuration:', error);
            setNotification({ message: 'Error deleting configuration.', type: 'error' });
        }
    };

    const toggleBotStatus = async (index) => {
        const newStatuses = [...botStatuses];
        const newStatus = !newStatuses[index];
        newStatuses[index] = newStatus;
        setBotStatuses(newStatuses);
        console.log("newStatuses ",newStatuses)
        const selectedSymbolsToTrade = selectedSymbols.length > 0 ? selectedSymbols : [tradingConfigurations[index].symbol];
        console.log("selectedSymbolsToTrade:", selectedSymbolsToTrade);

        try {
            for (const symbol of selectedSymbolsToTrade) {
                const response = await axios.post('http://localhost:7000/getTradingParams', { symbol });
                const tradingParams = response.data;
                console.log("trading Configuration", tradingParams);

                if (newStatus) {
                    await axios.post('http://localhost:5000/executeTrade', { ...tradingParams });
                    console.log(`Trade executed successfully for ${symbol} with params:`, tradingParams);
                } else {
                    console.log(`Bot for ${symbol} is inactive. No trade executed.`);
                }
            }
        } catch (error) {
            setNotification({ message: 'Error executing trade.', type: 'error' });
            console.error('Error executing trade:', error);
        }

        try {
            for (const symbol of selectedSymbolsToTrade) {
                const response = await axios.patch(`http://localhost:7000/updateInactive/${symbol}`);
                console.log('Updated Configuration:', response.data);
            }
        } catch (error) {
            setNotification({ message: 'Error updating configuration.', type: 'error' });
            console.error('Error updating configuration:', error);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

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

        const timeframeMapping = {
            M1: 1,
            M5: 5,
            M15: 15,
            M30: 30,
            H1: 60,
        };
        
        const mt5TimeFrame = timeframeMapping[timeFrame];

        const newConfiguration = {
            symbol: selectedSymbol.value,
            takeProfit: parseFloat(takeProfit),
            lotSize: parseFloat(lotSize),
            timeFrame: mt5TimeFrame
        };
        const token = localStorage.getItem('token'); 
        console.log("token ",token)
        try {
            await axios.post('http://localhost:7000/save', newConfiguration,{headers: {
                'Authorization': `Bearer ${token}`
            }});
            setTradingConfigurations([...tradingConfigurations, newConfiguration]);
            setNotification({ message: 'Settings saved successfully!', type: 'success' });
        } catch (error) {
            setNotification({ message: 'Error saving settings.', type: 'error' });
            console.error('Error posting settings:', error);
        }
        
        try {
            await axios.post('http://localhost:5000/saveSettings', newConfiguration);
            console.log("Settings saved to MetaTrader backend");
        } catch (error) {
            setNotification({ message: 'Error saving settings to MetaTrader backend.', type: 'error' });
            console.error('Error posting settings to MetaTrader backend:', error);
        }

        setShowForm(false);
        event.target.reset();
    };

    const filteredConfigurations = tradingConfigurations.filter(config =>
        config.symbol.toLowerCase().includes(searchTerm.toLowerCase())
    );
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = filteredConfigurations.slice(indexOfFirstItem, indexOfLastItem);
    useEffect(() => {
         setTotalItems(filteredConfigurations.length);
     }, [filteredConfigurations]);
    
    const isButtonDisabled = (index) => {
        // Vérifiez si l'élément est sélectionné
        return botStatuses[index];
    };
    
    const handlePageChange = (newPage) => {
        console.log("éhgjhgjh")
        if (newPage > 0 && newPage <= Math.ceil(totalItems / itemsPerPage)) {
            console.log("kkzjdkzaje")
            setCurrentPage(newPage);
        }
    };
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (formRef.current && !formRef.current.contains(event.target)) {
                setShowForm(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [formRef]);
    return (
        <div className="settings-container">
            <h1>Liste des Symboles</h1>
            <div className="table-controls">
            <div className="button-container">
    <button onClick={() => setShowForm(true)} className="open-form-btn">
        <FontAwesomeIcon icon={faPlusCircle} />
        <span className="tooltip">Ajouter symbole</span>
    </button>
</div>

                
                <div className="container">
                <input
                    type="text"
                    placeholder="Search..."
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                    className="search-input"
                />
            </div>
            </div>

            {showForm && (
                <div className="form-popup">
                    <form onSubmit={handleSubmit} ref={formRef}>
                        <label>
                            Symbol:
                            <Select
                                value={selectedSymbol}
                                onChange={setSelectedSymbol}
                                options={symbols}
                                className="basic-single"
                                classNamePrefix="select"
                            />
                        </label>
                        <label>
                            Lot Size:
                            <input type="number" value={lotSize} onChange={e => setLotSize(e.target.value)} />
                        </label>
                        <label>
                            Take Profit:
                            <input type="number" value={takeProfit} onChange={e => setTakeProfit(e.target.value)} />
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
                        <Notification message={notification.message} type={notification.type} />
                        <button type="submit">Save Settings</button>
                    </form>
                </div>
            )}

            <table>
                <thead>
                    <tr>
                        <th>Select</th> 
                        <th>Symbol</th>
                        <th>Lot Size</th>
                        <th>Take Profit</th>
                        <th>Time Frame</th>
                        <th>Actions</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {currentItems.map((config, index) => (
                        <tr key={config._id || index}>
                            <td>
                                <input 
                                    type="checkbox"
                                    checked={botStatuses[index]}
                                    onChange={() => toggleBotStatus(index)}
                                />
                            </td>
                            <td>{config.symbol}</td>
                            <td>{config.lotSize.toFixed(2)}</td>
                            <td>{config.takeProfit.toFixed(2)}</td>
                            <td>{config.timeFrame}</td>
                            <td>
                                <button className="edit" disabled={isButtonDisabled(index)}onClick={() => onEditClick(index)} title="Edit">
                                    <FontAwesomeIcon icon={faEdit} />
                                </button>
                                {' '}
                                <button className="delete" disabled={isButtonDisabled(index) } onClick={() => onDeleteClick(config._id)} title="Delete">
                                    <FontAwesomeIcon icon={faTrashAlt} />
                                </button>
                                <button
                                    className={`status-btn ${botStatuses[index] ? 'inactive' : 'active'}`}
                                >
                                    {botStatuses[index] ? 'Active' : 'Inactive'}
                                </button>
                            </td>
                            <td>
                            {botStatuses[index] ?  (<FontAwesomeIcon icon={faCheckCircle} className="status-icon active" style={{ color: 'green' }} />
                            ) : (
                                <FontAwesomeIcon icon={faTimesCircle} className="status-icon inactive" style={{ color: 'red' }} />
                            )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="pagination">
            <button className='prev' onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
                Previous
            </button>
            <span className="page-info">Page {currentPage} of {Math.ceil(totalItems / itemsPerPage)}</span>
            <button className='next' onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === Math.ceil(totalItems / itemsPerPage)}>
                Next
            </button>
        </div>

        </div>
    );
}

export default TradingSettings;
