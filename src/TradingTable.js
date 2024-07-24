import React , { useState }from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrashAlt, faPlusCircle } from '@fortawesome/free-solid-svg-icons';
import './styles.css';
import TradingForm from './TradingForm';



function TradingTable({ symbols, onEditClick, onDeleteClick }) {
  const [showForm, setShowForm] = useState(false);

  const handleSave = (formData) => {
    console.log('Form Data:', formData);
    // Handle save logic here
  };
  return (
    
    <table>
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Takefksdkfjs Profit</th>
          <th>Lot Size</th>
          <th>Stop Loss</th>
          <th>Time Frame</th>
          <th>Status</th> {/* Ajout d'une colonne de statut */}
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
      <div>
      
    </div>
        {symbols.map((symbol, index) => (
          <tr key={index}>
            <td>{symbol.symbol}</td>
            <td>{symbol.takeProfit}</td>
            <td>{symbol.lotSize}</td>
            <td>{symbol.stopLoss}</td>
            <td>{symbol.timeFrame}</td>
            <td>Status</td> {/* Ajout d'une colonne de statut */}
            <td>
              {/* Affichage du statut sous forme de cercle coloré */}
              <span className="status-indicator" style={{ backgroundColor: symbol? 'green' : 'red' }}></span>
            </td>
            <td>
              <button onClick={() => onEditClick(index)} title="Edit">
                <FontAwesomeIcon icon={faEdit} />
              </button>
              {' '}
              <button onClick={() => onDeleteClick(index)} title="Delete">
                <FontAwesomeIcon icon={faTrashAlt} />
              </button>
              <button onClick={() => toggleBotStatus(index)} title="Toggle Bot Status">
                  <FontAwesomeIcon icon={faPlusCircle} />
                </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TradingTable;
