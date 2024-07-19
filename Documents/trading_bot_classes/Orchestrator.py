import MetaTrader5 as mt5
import time
from datetime import datetime
import threading
import pandas as pd
class Orchestrator:
    def __init__(self, explorer, decider, executor,time_frame):
        self.explorer = explorer
        self.decider = decider   
        self.executor = executor
        self.time_frame=time_frame
       
      
    def monitor_positions(self):
        symbole2 = "EURAUD"
        sl_nouveau=0
        


        
        i=0
        while True:
            #le time frame du symbol
            periode2 = mt5.TIMEFRAME_M1
            prix2 = mt5.copy_rates_from_pos(symbole2, periode2, 0, 200)
            df2 = pd.DataFrame(prix2)
            periode1 = mt5.TIMEFRAME_M5
            prix1 = mt5.copy_rates_from_pos(symbole2, periode1, 0, 200)
            df1 = pd.DataFrame(prix2)
            print(i)
            i=i+1
            print("close 199 ",df2['close'][199])
            print("close 198 ",df2['close'][198])
            print("coucocuocu")
            try:
                print("nounou")
                if not mt5.initialize():
                    print("Échec de l'initialisation de MT5")
                    mt5.shutdown()
                positionss = mt5.positions_get(symbol=symbole2)
                print("posiotn",positionss)
                decision = self.decider.decide(df1,df2)
                if decision=="deplacer_sl"  :
                    self.executor.Deplacer_sl(self.explorer.symbol,'rzrazr')
                    self.executor.compteur=self.executor.compteur+1
                    if positionss:
                        print('il ya des posiotns')
                        for positions in positionss:
                            if positions.profit > 0:
                                print("positions.profit ",positions.profit)
                                if positions.type == mt5.ORDER_TYPE_BUY:
                                    print("sl nouveau est ",positions.price_open+15*mt5.symbol_info(symbole2).point)
                                    print("ticket is ",positions.ticket)
                                    sl_nouveau=positions.price_open+15*mt5.symbol_info(symbole2).point*i
                                    if positions.price_open+15*mt5.symbol_info(symbole2).point*i>=mt5.symbol_info_tick(symbole2).bid:
                                        sl_nouveau=mt5.symbol_info_tick(symbole2).bid
                                        i=i-1
                                    request = {
                                            "action": mt5.TRADE_ACTION_SLTP,
                                            "symbol": symbole2,
                                            "sl": sl_nouveau,
                                            "position": positions.ticket,
                                            "type_time": mt5.ORDER_TIME_GTC,
                                            "type_filling": mt5.ORDER_FILLING_IOC,
                                            }
                                    i=i+1
                                    result = mt5.order_send(request)
                                    if result.retcode != mt5.TRADE_RETCODE_DONE:
                                            print("Échec de la mise à jour du stop loss pour le ticket", positions.ticket, mt5.last_error())
                                    else:
                                        print("Stop loss mis à jour pour le ticket", positions.ticket)
                                elif positions.type == mt5.ORDER_TYPE_SELL:
                                    print("sl nouveau est ",positions.price_open-15*mt5.symbol_info(symbole2).point)
                                    if positions.price_open-15*mt5.symbol_info(symbole2).point*i<mt5.symbol_info_tick(symbole2).ask:
                                        sl_nouveau=mt5.symbol_info_tick(symbole2).ask
                                        i=i-1
                                    request = {
                                            "action": mt5.TRADE_ACTION_SLTP,
                                            "symbol": positions.symbol,
                                            "sl": sl_nouveau,
                                            "position": positions.ticket,
                                            "type_time": mt5.ORDER_TIME_GTC,
                                            "type_filling": mt5.ORDER_FILLING_IOC,
                                            }
                                    result = mt5.order_send(request)
                                    i=i+1
                                    if result.retcode != mt5.TRADE_RETCODE_DONE:
                                            print("Échec de la mise à jour du stop loss pour le ticket", positions.ticket, mt5.last_error())
                                    else:
                                        print("Stop loss mis à jour pour le ticket", positions.ticket)  
                            
                                            
                else:
                    print("Aucune position ouverte.")
                time.sleep(10)  # Pause pour réduire la charge
            except Exception as e:
                print("Erreur lors de la surveillance des positions :", str(e))
                time.sleep(60)  # Pause plus longue en cas d'erreur
    def demarrer_cycle(self):
        while True:  
            tf1=0
           
            print("self.explorer.timeframe ",self.explorer.timeframe)
            if(self.explorer.timeframe==mt5.TIMEFRAME_M5):
                tf1=mt5.TIMEFRAME_M1
                print("perioedin kllllllllllllllllllllis ", tf1)
            elif(self.explorer.timeframe==mt5.TIMEFRAME_M15) :
                
                tf1=mt5.TIMEFRAME_M5
                print("perioedin kkkkkkkkkkkkkkkkkkkkkkkkis ", tf1)
            start_time=datetime.now()
            print(f"[{datetime.now()}] Démarrage212 du cycle")
            print("self.explorer.timeframec",self.explorer.timeframe)# Affiche la date et l'heure actuelle à chaque cycle
            data=self.explorer.fetch_market_data(self.explorer.timeframe)
            print(data)
            data1=self.explorer.fetch_market_data(tf1)
           
          
            df = self.explorer.calculate_ichimoku(data)
            df1= self.explorer.calculate_ichimoku(data1)
            print("ishimoku ",df)
            print("chikou dernier ",df['chikou_span'][200-27])
            decision = self.decider.decide(df,df1)
            print("decision is ",decision)
            

            if decision == "buy":
                ask = mt5.symbol_info_tick(self.explorer.symbol).ask
                
                sl = df['kijun_sen'][199]
                tp = ask + self.executor.take_profit * mt5.symbol_info(self.explorer.symbol).point
               
                print("self.executor.take_profit ",self.executor.take_profit)
                self.executor.envoyer_ordre_achat(df)
                self.decider.close_threshold_val_buy = (ask - df['kijun_sen'][199]) + ask 
                print('self.decideur.close_threshold_val_buy ',self.decider.close_threshold_val_buy)
                
            elif decision == "sell":
                bid = mt5.symbol_info_tick(self.explorer.symbol).bid
                sl = df['kijun_sen'][199]
                print("sl is ",sl)
                tp = mt5.symbol_info(self.explorer.symbol).bid - self.executor.take_profit * mt5.symbol_info(self.explorer.symbol).point
                print("tp is ",tp)
                print("take profit  ",self.executor.take_profit )
                self.executor.envoyer_ordre_vente(df)
                self.decider.close_threshold_val_sell = bid-(df['kijun_sen'][199]-bid) 
                print('self.decideur.close_threshold_val_sell ',self.decider.close_threshold_val_sell)

            elif decision == "close_buy" :
                position = mt5.positions_get(symbol=self.explorer.symbol)
                print('decision c ',decision)
                self.executor.close_buy_positions(self.explorer.symbol,'coucou')
            elif decision == "close_sell" :  
                 position = mt5.positions_get(symbol=self.explorer.symbol)
                 self.executor.close_sell_positions(self.explorer.symbol,'coucou') 
            elif decision=="deplacer_sl"  :
                self.executor.Deplacer_sl(self.explorer.symbol,'rzrazr')
                self.executor.compteur=self.executor.compteur+1
                   
            else:
                print("no buy no sell no close")   
            elapsed_time = (datetime.now() - start_time).total_seconds()

            # Calcul du temps de sommeil restant pour faire exactement une minute
            sleep_time = max(0, 300 - elapsed_time)  # S'assurer que le sleep_time n'est pas négatif
            time.sleep(sleep_time)    
           
            mt5.shutdown()
    def demarrer(self):
        thread = threading.Thread(target=self.demarrer_cycle)  # Corrected
        thread.start()
