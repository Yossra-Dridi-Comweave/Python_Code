import MetaTrader5 as mt5

class Executor:
    def __init__(self, symbole, lot_size,take_profit,prix_risque,compteur):
        self.symbole = symbole
        self.lot_size=lot_size
        self.take_profit = take_profit
        
        self.prix_risque=prix_risque
        self.compteur=compteur
     
        
    def is_currency_pair(self,symbol):
     symbol_info = mt5.symbol_info(symbol)
    # Vérifiez si le chemin contient 'Forex' ou 'FX'
     if 'Forex' in symbol_info.path :
        return True
     return False
    def envoyer_ordre_achat(self,df):
        pips=0
        print("self.symbol ",self.symbole)
        point= mt5.symbol_info(self.symbole).point
        y=mt5.symbol_info_tick(self.symbole).ask
        if(self.is_currency_pair(self.symbole)):
              pips = abs( y- df['kijun_sen'][199]) / point
              print("pips are ",pips)
              self.lot_size=round(((self.prix_risque * mt5.symbol_info_tick(self.symbole).ask )/(round(pips,0)*mt5.symbol_info(self.symbole).point))/100000,2)
      
        
       
        print("take profit is" ,mt5.symbol_info_tick(self.symbole).ask + point * self.take_profit)
        
        request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": self.symbole,
        "volume": self.lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": y,
        "sl": df['kijun_sen'][199],
        "tp": y + point * self.take_profit ,  
        "magic": 234000,
        "comment": "Ichimoku buy order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order failed, retcode={}".format(result.retcode))
        else:
            print("Order executed successfully")
        close_threshold_val_buy = (y-df['kijun_sen'][199])+y 
        print("closethreshold pour buy est ", close_threshold_val_buy)
        
    def envoyer_ordre_vente(self,df):
        point= mt5.symbol_info(self.symbole).point
        pips=0
        print("kijun ",df['kijun_sen'][199])
        print("ask ",mt5.symbol_info_tick(self.symbole).ask)
        print("symbole ",self.symbole)
        y=mt5.symbol_info_tick(self.symbole).bid
        pips = abs( y- df['kijun_sen'][199]) / point
        print("pips are ",pips)
        if(self.is_currency_pair(self.symbole)):
             self.lot_size=round(((self.prix_risque * mt5.symbol_info_tick(self.symbole).bid )/(round(pips,0)*mt5.symbol_info(self.symbole).point))/100000,2)
      
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbole,
            "volume": self.lot_size,
            "type": mt5.ORDER_TYPE_SELL,
            "price": y,
            "sl": df['kijun_sen'][199],
            "tp": mt5.symbol_info_tick(self.symbole).bid - point * self.take_profit,
            "magic": 234000,
            "comment": "Ichimoku sell order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        close_threshold_val_sell=y-(df['kijun_sen'][199]-y) 
        print("close threshold pour sell est ", close_threshold_val_sell )   
    
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order failed, retcode={}".format(result.retcode))
        else:
            print("Order executed successfully")
        
    def close_sell_positions(self,symbol, comment):

    # Récupérer toutes les positions ouvertes pour le symbole donné
        positions = mt5.positions_get(symbol=symbol)
        if positions:
            for position in positions:
                if position.type == mt5.ORDER_TYPE_SELL:
                    # Obtenir le prix actuel pour le symbole à l'ask
                    price = mt5.symbol_info_tick(symbol).ask

                    # Préparation de la demande de clôture de la position
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": position.volume,
                        "type": mt5.ORDER_TYPE_BUY,
                        "position": position.ticket,
                        "price": price,
                        "deviation": 10,
                        "magic": 0,
                        "comment": comment,
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_IOC,
                    }
                    
                    # Envoyer la demande de clôture
                    result = mt5.order_send(request)
                    if result.retcode != mt5.TRADE_RETCODE_DONE:
                        print(f"Échec de la fermeture de la position {position.ticket}: {result.retcode}")
                    else:
                        print(f"Position {position.ticket} fermée avec succès")
        else:
            print(f"Aucune position ouverte à fermer pour le symbole {symbol}.")

    def close_buy_positions(self,symbol, comment):
        print('onv afreemererere')
        # Récupérer toutes les positions ouvertes pour le symbole donné
        positions = mt5.positions_get(symbol=symbol)
        print("paodioernerineo")
        if positions:
            for position in positions:
                print("paodioernerineo???????????")
                # Vérifier si la position est un achat
                print('position.type ',position.type)
                if position.type == mt5.ORDER_TYPE_BUY:
                    # Obtenir le prix actuel pour le symbole
                    print("paodioernerineo???????????dqsdqsdqd")
                    price = mt5.symbol_info_tick(symbol).bid
                    
                    # Préparation de la demande de clôture de la position
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": position.volume,
                        "type": mt5.ORDER_TYPE_SELL,
                        "position": position.ticket,
                        "price": price,
                        "deviation": 10,
                        "magic": 0,
                        "comment": comment,
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_IOC,
                    }
                    
                    # Envoyer la demande de clôture
                    result = mt5.order_send(request)
                    if result.retcode != mt5.TRADE_RETCODE_DONE:
                        print(f"Échec de la fermeture de la position {position.ticket}: {result.retcode}")
                    else:
                        print(f"Position {position.ticket} fermée avec succès")
        else:
            print(f"Aucune position ouverte à fermer pour le symbole {symbol}.")
    
    def Deplacer_sl(self,symbol, comment):
       
        positionss = mt5.positions_get(symbol=symbol)
        print("posiotn",positionss)
          
        sl_nouveau=positionss[0].price_open+15*mt5.symbol_info(symbol).point*self.compteur
        if positionss[0].type == mt5.ORDER_TYPE_BUY:
            sl_nouveau=positionss[0].price_open+15*mt5.symbol_info(symbol).point*self.compteur
            if positionss[0].price_open+15*mt5.symbol_info(symbol).point*self.compteur>=mt5.symbol_info_tick(symbol).bid:
                sl_nouveau=mt5.symbol_info_tick(symbol).bid
                self.compteur=self.compteur-1
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": symbol,
                "sl": sl_nouveau,
                "position": positionss[0].ticket,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
                    }
        
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Échec de la mise à jour du stop loss pour le ticket", positionss[0].ticket, mt5.last_error())
            else:
                print("Stop loss mis à jour pour le ticket", positionss[0].ticket)
        elif positionss[0].type == mt5.ORDER_TYPE_SELL:
            sl_nouveau=positionss[0].price_open-15*mt5.symbol_info(symbol).point*self.compteur
            print("sl nouveau est ",positionss[0].price_open-15*mt5.symbol_info(symbol).point)
            if positionss[0].price_open-15*mt5.symbol_info(symbol).point*self.compteur<mt5.symbol_info_tick(symbol).ask:
                sl_nouveau=mt5.symbol_info_tick(symbol).ask
                self.compteur==self.compteur-1
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": positionss[0].symbol,
                "sl": sl_nouveau,
                "position": positionss[0].ticket,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
                    }
            result = mt5.order_send(request)
        
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Échec de la mise à jour du stop loss pour le ticket", positionss[0].ticket, mt5.last_error())
            else:
                print("Stop loss mis à jour pour le ticket", positionss[0].ticket)  