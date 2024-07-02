import MetaTrader5 as mt5

class Executor:
    def __init__(self, symbole,lot_size, take_profit, stop_loss):
        self.symbole = symbole
        self.lot_size = lot_size
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        

    def envoyer_ordre_achat(self,prix, sl, df,tp):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbole,
            "volume": self.lot_size,
            "type": mt5.ORDER_TYPE_BUY,
            "price": prix,
            "sl": sl,
            "tp": tp,
            "magic": 234000,
            "comment": "Ichimoku buy order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        close_threshold_val_buy = ((prix-df['kijun_sen'][199])/2)+prix 
        print("closethreshold pour buy est ", close_threshold_val_buy)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order failed, retcode={}".format(result.retcode))
        else:
            print("Order executed successfully")
        
    def envoyer_ordre_vente(self, prix, sl,df, tp):
        print('sl ou',sl)
        print('tp ou ',tp)
        print("bid ou ",prix)
        print("kijun ",df['kijun_sen'][199])
        print("ask ",mt5.symbol_info_tick(self.symbole).ask)
        print("symbole ",self.symbole)
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbole,
            "volume": self.lot_size,
            "type": mt5.ORDER_TYPE_SELL,
            "price": prix,
            "sl": df['kijun_sen'][199],
            "tp": tp,
            "magic": 234000,
            "comment": "Ichimoku sell order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        close_threshold_val_sell=prix-((df['kijun_sen'][199]-prix)/2) 
        print("close threshold pour sell est ", close_threshold_val_sell )   
    
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order failed, retcode={}".format(result.retcode))
        else:
            print("Order executed successfully")
        
    def fermer_position(self,positions,type):
      
        if positions:
            position = positions[0]
            
            print("type ",type)
            order_type = mt5.ORDER_TYPE_SELL if type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbole,
                "volume": position.volume,
                "type": order_type,
                "position": position.ticket,
                "price": mt5.symbol_info_tick(self.symbole).bid if order_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(self.symbole).ask,
                "magic": 234000,
                "comment": "Close order",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Close order failed, retcode={}".format(result.retcode))
            else:
                print("Close order executed successfully")
        
