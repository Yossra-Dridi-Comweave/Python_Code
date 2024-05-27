import MetaTrader5 as mt5 # type: ignore
import pandas as pd # type: ignore
import time
#le symbol qu'on va travailler sur
symbole = "AUDJPY"
#le time frame du symbol
periode = mt5.TIMEFRAME_M1
#take_profit
take_profit=300
#stop_loss
stop_loss=50
#lot_size
lot_size=0.1
#closethreshold
close_threshold_val_sell=0
close_threshold_val_buy=0
#borne_inf_rsi
borne_inf_rsi=10
#borne_sup_rsi
borne_sup_rsi=90
#Recuperer des informations sur le symbol
symbol_info = mt5.symbol_info(symbole)

#calcul du second indicateur qui va nous aider à renforcer notre prise de decision

def calculate_rsi(prices, period=14):
    # Calculer les différences de clôture
    delta = prices.diff()

    # Séparer les gains et les pertes
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculer les gains et les pertes moyens
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Calculer le RS (Relative Strength)
    rs = avg_gain / avg_loss

    # Calculer le RSI
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Une fonction qui va nous aider à Obtenir toutes les positions ouvertes
def get_positions_for_symbol(symbol):
   
    positions = mt5.positions_get()
    if positions is None:
        print("NO positions opened")
        return []
    
    # Filtrer les positions pour le symbole spécifique
    filtered_positions = [pos for pos in positions if pos.symbol == symbol]
    return filtered_positions

#ici on va commencer 
while(True):
    
    #on commencer par une initialisation du metatrader5
    if not mt5.initialize():
        print("Initialisation de MT5 a échoué")
        mt5.shutdown()
    #on va obtenir toutes les positions ouvertes de notre symbole
    positions_opened = get_positions_for_symbol(symbole)  
    #on va obtenir touttes les symboles disponibles  
    
    
   
    symbols=mt5.symbols_get()
    print('Symbols: ', len(symbols))
    symbol_info = mt5.symbol_info(symbole)
    point=symbol_info.point
    print("le point est ",point)
   
    # On va Télécharger les données historiques de 1000 bougies
    prix = mt5.copy_rates_from_pos(symbole, periode, 0, 1000)
    
    positions = get_positions_for_symbol(symbole)
    if(positions):
     for position in positions:
                symbol = position.symbol
                volume = position.volume
                print("prix de d'ouverture de la position est ",position.price_open)
    # Convertir en DataFrame
    df = pd.DataFrame(prix)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # Calcul des lignes Ichimoku
    df['tenkan_sen'] = (df['high'].rolling(window=9).max() + df['low'].rolling(window=9).min()) / 2
    df['kijun_sen'] = (df['high'].rolling(window=26).max() + df['low'].rolling(window=26).min()) / 2
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
    df['senkou_span_b'] = ((df['high'].rolling(window=52).max() + df['low'].rolling(window=52).min()) / 2).shift(26)
    df['chikou_span'] = df['close'].shift(-26)

    #calcul de rsi
    rsi_values = calculate_rsi(df['close'][986:1000], period=14)
    print("rsi de la derniere bougie est ",rsi_values[999])
    
    
    
    # Affichage des valeurs de lignes ishimoku pour les 30 derniere bougies
    print(df[['time', 'tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']].tail(30))
   
     
    #Conditions à verifier pour OUVRIR une POSITION LONGUE
    
    condition1_chikou_and_close_buy=df['chikou_span'][1000-27]>df['close'][1000-27]
    condition2_tenkan_chikou_buy=df['chikou_span'][1000-27]>df['tenkan_sen'][1000-27]
    condition3_kijun_chikou_buy=df['chikou_span'][1000-27]>df['kijun_sen'][1000-27]
    condition4_ssb_ssa_chikou_buy=df['chikou_span'][1000-27]>df['senkou_span_b'][1000-27] and df['chikou_span'][1000-27]>df['senkou_span_a'][1000-27]
    condition5_tenkan_kijun_buy=df['tenkan_sen'][999]>df['kijun_sen'][999]
    condition6_ssb_kijun_buy=df['kijun_sen'][999]>df['senkou_span_b'][999]
    condition7_close_open_buy=df['close'][999]>df['open'][999]
    condition8_tenkan_prix_buy=df['tenkan_sen'][999]<df['low'][999]
    
    condition10_positions_opened=len(positions_opened) == 0 
    condition11_prix_nuage_buy=df['low'][999]>df['senkou_span_b'][999] and df['low'][999]>df['senkou_span_a'][999] 
    #la condition finale d'ouverture d'une posiotn longue
    buy_condition= (condition10_positions_opened and condition11_prix_nuage_buy and condition1_chikou_and_close_buy and condition8_tenkan_prix_buy and condition2_tenkan_chikou_buy and condition3_kijun_chikou_buy and condition4_ssb_ssa_chikou_buy and condition5_tenkan_kijun_buy and condition6_ssb_kijun_buy and condition7_close_open_buy)
    #Affichage des conditions
    print("condition1 chikou et close buy ",condition1_chikou_and_close_buy)
    print("condition2 tenkan et close buy ",condition2_tenkan_chikou_buy)
    print("condition3 kijun et chikou buy ",condition3_kijun_chikou_buy)
    print("condition4 buy ssb et chikou ",condition4_ssb_ssa_chikou_buy)
    print("condition5 buy tenkan et kijun ",condition5_tenkan_kijun_buy)
    print("condition6 buy ssb et kijun ",condition6_ssb_kijun_buy)
    print("condition7 buy close et open ",condition7_close_open_buy)
    print("condition8_tenkan_prix_buy",condition8_tenkan_prix_buy)
    print("condition10_positions_opened",condition10_positions_opened)
    print("condition11_prix_nuage_buy ",condition11_prix_nuage_buy)
    print("condition_buy ",buy_condition)
    #verfication des condiotions d'achat et execution du requete si les conditions sont verifiées
    if (buy_condition):
        y=mt5.symbol_info_tick(symbole).ask
        x=mt5.symbol_info_tick(symbole).ask + point * take_profit
        open_price = mt5.symbol_info_tick(symbole).ask
        print("take profit is" ,mt5.symbol_info_tick(symbole).ask + point * take_profit)
        #point= mt5.symbol_info_tick(symbole).point
        request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbole,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": y,
        "sl": df['kijun_sen'][999],
        "tp": y + point * take_profit ,  
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
        close_threshold_val_buy = (df['kijun_sen'][999]+y)/2 
        print("closethreshold pour buy est ", close_threshold_val_buy)
    else:
        print("non les condtions d'achat ne sont pas verifiées")        


    

            

    #Conditions à verifier pour ouvrir une position courte
    condition1_chikou_and_close_sell=df['close'][1000-27]>df['chikou_span'][1000-27]
    condition2_chikou_tenkan_sell=df['chikou_span'][1000-27]<df['tenkan_sen'][1000-27]
    condition3_kijun_chikou_sell=df['chikou_span'][1000-27]<df['kijun_sen'][1000-27]
    condition4_ssb_chikou_sell=df['chikou_span'][1000-27]<df['senkou_span_b'][1000-27]
    
    condition8_prix_tenkan=df["tenkan_sen"][999] > df['high'][999]
    condition5_tenkan_kijun_sell=df['tenkan_sen'][999]<df['kijun_sen'][999]
    condition11_prix_nuage_sell=df['high'][999]<df['senkou_span_b'][999] and df['high'][999]<df['senkou_span_a'][999] 
    condition6_ssb_kijun_sell=df['kijun_sen'][999]<df['senkou_span_b'][999]
    condition7_close_open_sell=df['close'][999]<df['open'][999]
    condition9_positions_ouvertes=len(positions_opened) == 0
    condition10_rsi_value=rsi_values[999]>=borne_sup_rsi
    #Condition finale pour ouvrir une position courte
    sell_condition=(condition9_positions_ouvertes and condition8_prix_tenkan  and condition1_chikou_and_close_sell and  condition11_prix_nuage_sell and condition2_chikou_tenkan_sell and condition3_kijun_chikou_sell and condition4_ssb_chikou_sell and condition5_tenkan_kijun_sell and condition6_ssb_kijun_sell  and condition7_close_open_sell )

    print("condition1 chikou et close ",condition1_chikou_and_close_sell)
    print("condition2 tenkan et close ",condition2_chikou_tenkan_sell)
    print("condition3 kijun et chikou ",condition3_kijun_chikou_sell)
    print("condition4 ssb et chikou",condition4_ssb_chikou_sell)
    print("condition5 tenkanet kijun ",condition5_tenkan_kijun_sell)
    print("condition8_prix_tenkan ",condition8_prix_tenkan)
    print("condition6 ssb et kijun ",condition6_ssb_kijun_sell)
    print("kijun ",df['kijun_sen'][999])
    print("ssb ",df['senkou_span_b'][999])
    print("condition7 open et close",condition7_close_open_sell)
    print("condition9_positions_ouvertes ",condition9_positions_ouvertes)
    print(" condition11_prix_nuage_sell ", condition11_prix_nuage_sell)
    print("condition_selll ",sell_condition)
    
    #Verification de la condition d'ouveture d'une position courte et execution de la requete si tout va bien
    if (sell_condition):
        y=mt5.symbol_info_tick(symbole).bid
        x=mt5.symbol_info_tick(symbole).bid - point * take_profit
        print( "y=mt5.symbol_info_tick(symbole).bid ", mt5.symbol_info_tick(symbole).bid)
        print( "x=mt5.symbol_info_tick(symbole).bid - point * take_profit ", mt5.symbol_info_tick(symbole).bid - point * take_profit)
        bid = mt5.symbol_info_tick(symbole).bid
        
        print("bid est ", bid)
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbole,
            "volume": lot_size,
            "type": mt5.ORDER_TYPE_SELL,
            "price": bid,
            "sl": df['kijun_sen'][999],
            "tp":mt5.symbol_info_tick(symbole).bid - point * take_profit ,
            "magic": 234000,
            "comment": "Ichimoku sell order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Execute the sell order
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Sell order failed", result.retcode)
        else:
            print("Sell order executed", result.order)
        close_threshold_val_sell=(df['kijun_sen'][999]+y)/2 
        print("close threshold pour sell est ", close_threshold_val_sell )   
    else:
        print("Les conditions d'ouverture d'un position courte ne sont pas verifiées")
    # 
    def close_sell_positions(comment):
    # Récupérer toutes les positions ouvertes
        positions = mt5.positions_get()
        if positions:
            for position in positions:
                symbol = position.symbol
                volume = position.volume
                if position.type == mt5.ORDER_TYPE_SELL:
               
                    price = mt5.symbol_info_tick(symbol).ask
                
                # Préparation de la demande de clôture de la position
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": volume,
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
            print("Aucune position ouverte à fermer.")
    def close_buy_positions(comment):
    # Récupérer toutes les positions ouvertes
        positions = mt5.positions_get()
        if positions:
            for position in positions:
                symbol = position.symbol
                volume = position.volume
                if position.type == mt5.ORDER_TYPE_BUY:
               
                    price = mt5.symbol_info_tick(symbol).bid
                
                # Préparation de la demande de clôture de la position
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": volume,
                        "type": mt5.ORDER_TYPE_SELL,
                        "position": position.ticket,
                        "price": price,
                        "deviation": 10,
                        "magic": 0,
                        "comment":comment,
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
            print("Aucune position ouverte à fermer.")        
    if(len(positions_opened) != 0 and mt5.symbol_info_tick(symbole).ask>=close_threshold_val_buy and round(df['chikou_span'][1000-27],4)>round(df["kijun_sen"][1000-27],4) and round(df['low'][999],4)<=round(df["tenkan_sen"][999],4) and round(df['high'][999],4)>=round(df["tenkan_sen"][999],4) and round(df['close'][999],4)<round(df['open'][999] ,4) ):
        print("2eme condition de cloture d'une position longue verifie")
        close_buy_positions("le close thrshold") 
    else:
       print("df['chikou_span'][1000-27]>df['kijun_sen'][1000-27] ",df['chikou_span'][1000-27]>df["kijun_sen"][1000-27])
       print("df['low'][999]<=df['tenkan_sen'][999] and df['high'][999]>=df['tenkan_sen'][999]",df['low'][999]<=df["tenkan_sen"][999] and df['high'][999]>=df["tenkan_sen"][999])
       print("la 2eme condition pour fermer une position longue ouverte n'est pas verifiée ")
       
    if(len(positions_opened) != 0 and round(df['chikou_span'][1000-27],4)<round(df['chikou_span'][1000-28],4) and round(df['chikou_span'][1000-27],4)<=round(df['kijun_sen'][1000-27],4) ):
        print("1ere condition de cloture d'une position longue verifie ")
        close_buy_positions("kijun et chikou inter")     
    else:
        print("la 1ere condition pour fermer une position longue ouverte n'est pas verifiée ")
    if(len(positions_opened) != 0 and mt5.symbol_info_tick(symbole).bid<=close_threshold_val_sell and round(df['chikou_span'][1000-27],4)<round(df["kijun_sen"][1000-27],4) and round(df['low'][999],4)<=round(df["tenkan_sen"][999],4) and round(df['high'][999],4)>=round(df["tenkan_sen"][999],4)  and round(df['close'][999],4)>round(df['open'][999],4)  ):
        print("2eme condition de cloture d'une position courte verifie")
        close_sell_positions("closethreshold atteint")
    else:
       print("la 2eme condition pour fermer une position courte ouverte n'est pas verifiée ")   
    if(len(positions_opened) != 0 and round(df['chikou_span'][1000-27],4)>round(df['chikou_span'][1000-28],4) and round(df['chikou_span'][1000-27],4)>=round(df['kijun_sen'][1000-27],4)) :
        print("1ere condition de cloture d'une position courte verifie ")
        close_sell_positions("kijun et chikou inter")
    else:
        print("la 1ere condition pour fermer une position courte ouverte n'est pas verifiée ")
    
    #Maintenant on va patienter une minutepour reexecuter le code precedent
    time.sleep(60)  
     
   
    mt5.shutdown()

   
