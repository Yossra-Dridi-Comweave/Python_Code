import MetaTrader5 as mt5
import time
from datetime import datetime
import threading
class Orchestrator:
    def __init__(self, analyseur, decideur, executeur):
        self.analyseur = analyseur
        self.decideur = decideur   
        self.executeur = executeur

    def demarrer_cycle(self):
        while True:  
            start_time=datetime.now()
            print(f"[{datetime.now()}] Démarrage du cycle")  # Affiche la date et l'heure actuelle à chaque cycle
            
            prix = self.analyseur.fetch_market_data()
            print("prices are ",prix)
            df = self.analyseur.calculate_ichimoku(prix)
            print("ishimoku ",df)
            print("chikou dernier ",df['chikou_span'][200-27])
            decision = self.decideur.decide_open(df)
            print("decioen is ",decision)
            self.decideur.bid= mt5.symbol_info_tick(self.analyseur.symbol).bid
            self.decideur.ask=mt5.symbol_info_tick(self.analyseur.symbol).ask

            if decision == "buy":
                ask = mt5.symbol_info_tick(self.analyseur.symbol).ask
                print("ask est ",ask)
                sl = df['kijun_sen'][199]
                tp = ask + self.executeur.take_profit * mt5.symbol_info(self.analyseur.symbol).point
                print("tp est ",tp)
                print("self.executeur.take_profit ",self.executeur.take_profit)
                self.executeur.envoyer_ordre_achat(ask, sl, df,tp)
                self.decideur.close_threshold_val_buy = ((ask - df['kijun_sen'][199]) / 2) + ask 
                print('self.decideur.close_threshold_val_buy ',self.decideur.close_threshold_val_buy)
                print("take profit  ",self.executeur.take_profit )
            elif decision == "sell":
                bid = mt5.symbol_info_tick(self.analyseur.symbol).bid
                sl = df['kijun_sen'][199]
                print("sl is ",sl)
                tp = mt5.symbol_info(self.analyseur.symbol).bid - self.executeur.take_profit * mt5.symbol_info(self.analyseur.symbol).point
                print("tp is ",tp)
                print("take profit  ",self.executeur.take_profit )
                self.executeur.envoyer_ordre_vente(bid, sl, df,tp)
                self.decideur.close_threshold_val_sell = bid-((df['kijun_sen'][199]-bid) / 2) 
                print('self.decideur.close_threshold_val_sell ',self.decideur.close_threshold_val_sell)

            elif decision == "close_long" :
                position = mt5.positions_get(symbol=self.analyseur.symbol)
                self.executeur.fermer_position(position,position[0].type)
            elif decision == "close_short" :  
                 position = mt5.positions_get(symbol=self.analyseur.symbol)
                 self.executeur.fermer_position(position,position[0].type)  
            else:
                print("no buy no sell no close")   
            elapsed_time = (datetime.now() - start_time).total_seconds()

            # Calcul du temps de sommeil restant pour faire exactement une minute
            sleep_time = max(0, 300 - elapsed_time)  # S'assurer que le sleep_time n'est pas négatif
            time.sleep(sleep_time)    
           
            mt5.shutdown()
    def demarrer(self):
        threading.Thread(target=self.demarrer_cycle).start()