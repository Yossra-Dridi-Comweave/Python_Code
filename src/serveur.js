const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const jwt = require('jsonwebtoken'); 
const app = express();
const port = 7000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

app.use(cors({
  origin: '*' // Autoriser toutes les origines
}));

// Modèle de données pour les paramètres de trading
const SettingsSchema = new mongoose.Schema({
  userId: String,
  symbol: String,
  takeProfit: Number,
  lotSize: Number,

  timeFrame: String,
  inactive: Boolean
});

const TradingSetting = mongoose.model('TradingSetting', SettingsSchema);

// Connexion à MongoDB
mongoose.connect('mongodb://127.0.0.1:27017/Trading_settings', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));

// Route pour enregistrer les paramètres
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (token == null) return res.sendStatus(401);

  jwt.verify(token, 'yossra_dridi', (err, user) => {
      if (err) return res.sendStatus(403);
      req.user = user;
      next();
  });
}
// Route pour enregistrer les paramètres
app.post('/save', authenticateToken, async (req, res) => {
  const { symbol, takeProfit, lotSize, timeFrame } = req.body;
  const userId = req.user.user_id;  // Extraire user_id du token
  console.log("useId ",userId)

  try {
      const newSetting = new TradingSetting({
          userId,  // Inclure userId
          symbol,
          takeProfit,
          lotSize,
          timeFrame,
          inactive: true
      });
      await newSetting.save();
      res.status(200).json({ message: 'Settings saved!' });
  } catch (error) {
      res.status(500).json({ message: 'Error saving settings.' });
  }
});
// Route pour supprimer une configuration de trading spécifique
app.delete('/delete/:id', async (req, res) => {
  const { id } = req.params;

  // Validation de l'ObjectId
  if (!mongoose.Types.ObjectId.isValid(id)) {
    return res.status(400).json({ message: 'Invalid ID format.' });
  }

  try {
    const result = await TradingSetting.findByIdAndDelete(id);
    if (!result) {
      return res.status(404).json({ message: 'Configuration not found' });
    }
    res.status(200).json({ message: 'Configuration deleted successfully' });
  } catch (error) {
    console.error('Error deleting configuration:', error);
    res.status(500).json({ message: 'Error deleting configuration' });
  }
});

app.get('/configurations', async (req, res) => {
  try {
    const configurations = await TradingSetting.find({});  // Utilise Mongoose pour récupérer toutes les configurations
    res.status(200).json(configurations);  // Renvoie les configurations au client
  } catch (error) {
    console.error('Failed to fetch configurations:', error);
    res.status(500).json({ message: 'Failed to fetch configurations' });
  }
});

app.post('/getTradingParams', async (req, res) => {
  const { symbol } = req.body;
  console.log("symbol received:", symbol); // Affiche le symbole reçu

  try {
      const config = await TradingSetting.findOne({ symbol }).select('-userId');;

      if (!config) {
          return res.status(404).json({ message: 'Trading configuration not found.' });
      }
  
      
      console.log("Trading configurations returned:", config);

      res.status(200).json(config);
  } catch (error) {
      console.error('Error fetching trading parameters:', error);
      res.status(500).json({ message: 'Error fetching trading parameters.' });
  }
});
app.patch('/updateInactive/:symbol', async (req, res) => {
  const { symbol } = req.params;
  console.log(`Received request to updateInactive for symbol: ${symbol}`);

  try {
    const updatedSetting = await TradingSetting.findOneAndUpdate(
      { symbol },  // Filtrer par le symbole
      { $set: { inactive: false } },  // Mettre à jour le champ inactive
      { new: true }  // Retourner le document mis à jour
    );

    if (!updatedSetting) {
      console.log(`No trading configuration found for symbol: ${symbol}`);
      return res.status(404).json({ message: 'Trading configuration not found.' });
    }

    console.log('Updated Configuration:', updatedSetting);
    res.status(200).json(updatedSetting);
  } catch (error) {
    console.error('Error updating inactive field:', error);
    res.status(500).json({ message: 'Error updating inactive field.' });
  }
});





// Exemple de backend avec Node.js et Express
app.get('/config', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const skip = (page - 1) * limit;

  try {
      const totalCount = await TradingSetting.countDocuments();
      const configurations = await TradingSetting.find()
          .skip(skip)
          .limit(limit);
      res.json({ configurations, totalCount });
  } catch (error) {
      res.status(500).json({ message: 'Error fetching configurations', error });
  }
});
app.post('/getTradingParamsForUser', async (req, res) => {
  const { userId } = req.body;

  try {
    const settings = await TradingSetting.find({ userId });
    if (settings.length === 0) {
      return res.status(404).json({ message: 'No trading settings found for this user.' });
    }
    res.status(200).json(settings);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching trading settings.' });
  }
});

// server.js
app.get('/getSettings', authenticateToken, async (req, res) => {
  try {
      const userId = req.user.user_id;  // Récupération de l'identifiant de l'utilisateur depuis le token
      console.log("userId ",userId)
      const settings = await TradingSetting.find({ userId });
      res.status(200).json(settings);
  } catch (error) {
      console.error('Error retrieving settings:', error);
      res.status(500).json({ status: 'error', message: 'Internal Server Error' });
  }
});

app.listen(port, () => console.log(`Server running on port ${port}`));
