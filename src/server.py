from flask import Flask, request, jsonify
import MetaTrader5 as mt5
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print("Received data:", data)
    username = data['username']
    password = data['password']
    server = data['server']

    # Initialisation de la connexion MT5
    if not mt5.initialize(login=int(username), password=password, server=server):
        print("Échec de la connexion à MetaTrader 5")
        return jsonify({"status": "error", "message": "Échec de la connexion"}), 500

    # Vérification du statut de connexion
    authorized = mt5.login(login=int(username), password=password, server=server)
    if not authorized:
        print("Autorisation échouée avec MT5")
        mt5.shutdown()
        return jsonify({"status": "error", "message": "Autorisation échouée"}), 401

    print("Connecté et autorisé.")
    mt5.shutdown()
    return jsonify({"status": "success", "message": "Connexion réussie!"})
@app.route('/symbols', methods=['GET'])
def get_symbols():
    if not mt5.initialize():
        return jsonify({"status": "error", "message": "Failed to initialize MT5"}), 500
    symbols = mt5.symbols_get()
    mt5.shutdown()
    return jsonify({"symbols": [symbol.name for symbol in symbols]})

if __name__ == '__main__':
    app.run(debug=True)
