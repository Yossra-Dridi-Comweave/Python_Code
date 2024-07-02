import MetaTrader5 as mt5
class Decider:
    def __init__(self, symbol, close_threshold_val_buy,ask,bid,close_threshold_val_sell):
         self.symbol=symbol
         
         self.close_threshold_val_buy=close_threshold_val_buy
         self.close_threshold_val_sell=close_threshold_val_sell
         self.ask=ask 
         self.bid=bid
      
        
       

    def decide_open(self,ichimoku_df):
        decision="no one"
        print(decision)
        if len(mt5.positions_get(symbol=self.symbol)) == 0:
            # Vérifier d'abord les conditions générales avant les conditions spécifiques plus coûteuses
            if ichimoku_df['chikou_span'][200-27] >  ichimoku_df['close'][200-27]:
                if ichimoku_df['chikou_span'][200-27] >  ichimoku_df['tenkan_sen'][200-27]:
                    if  ichimoku_df['chikou_span'][200-27] >  ichimoku_df['kijun_sen'][200-27]:
                        if  ichimoku_df['chikou_span'][200-27] >  ichimoku_df['senkou_span_b'][200-27] and  ichimoku_df['chikou_span'][200-27] >  ichimoku_df['senkou_span_a'][200-27]:
                            if  ichimoku_df['tenkan_sen'][199] >  ichimoku_df['kijun_sen'][199]:
                                if  ichimoku_df['kijun_sen'][199] >  ichimoku_df['senkou_span_b'][199]:
                                    if  ichimoku_df['close'][199] >  ichimoku_df['open'][199]:
                                        if  ichimoku_df['tenkan_sen'][199] <  ichimoku_df['low'][199]:
                                            if  ichimoku_df['low'][199] >  ichimoku_df['senkou_span_b'][199] and  ichimoku_df['low'][199] >  ichimoku_df['senkou_span_a'][199]:
                                                decision="buy"
                                                return decision
                                            else:
                                                 print("buy not done")  
                                        else:
                                            print("tenkan et high buy") 
                                    else:
                                            print("open et clsoe buy")   
                                else:
                                            print("kijun et ssb buy")   
                            else:
                                            print("tenkan et kijun buy")   
                        else:
                                            print("chikou,ssb et ssa buy") 
                                            print("chikou ",ichimoku_df['chikou_span'][200-27]) 
                                            print("spanb ",ichimoku_df['senkou_span_b'][200-27])  
                                            
                                            print("sapna ",ichimoku_df['senkou_span_a'][200-27])
                    else:
                                            print("kijun et chikou buy")   
                else:
                                            print("tenkan et chikou buy")                                                                                                                  
            else:
                print("close et chikou buy")
        else:
                print("nonon")                                
      
        # Similaire pour les conditions de vente
        if len(mt5.positions_get(symbol=self.symbol)) == 0:
          
            if  ichimoku_df['close'][200-27] >  ichimoku_df['chikou_span'][200-27]:
                if  ichimoku_df['tenkan_sen'][200-27] >  ichimoku_df['chikou_span'][200-27]:
                    if  ichimoku_df['kijun_sen'][200-27] >  ichimoku_df['chikou_span'][200-27]:
                        if  ichimoku_df['senkou_span_b'][200-27] >  ichimoku_df['chikou_span'][200-27] and  ichimoku_df['senkou_span_a'][200-27] >  ichimoku_df['chikou_span'][200-27]:
                            if  ichimoku_df['tenkan_sen'][199] <  ichimoku_df['kijun_sen'][199]:
                                if  ichimoku_df['kijun_sen'][199] <  ichimoku_df['senkou_span_b'][199]:
                                    if  ichimoku_df['open'][199] >  ichimoku_df['close'][199]:
                                        if  ichimoku_df['tenkan_sen'][199] >  ichimoku_df['high'][199]:
                                            if  ichimoku_df['high'][199] <  ichimoku_df['senkou_span_b'][199] and  ichimoku_df['high'][199] <  ichimoku_df['senkou_span_a'][199]:
                                                
                                                decision="sell"
                                                return decision
                                            else:
                                                 print("sell not done")  
                                        else:
                                            print("tenkan et high sell") 
                                    else:
                                            print("open et clsoe sell")   
                                else:
                                            print("kijun et ssb sell")   
                            else:
                                            print("tenkan et kijun sell")   
                        else:
                                            print("chikou,ssb et ssa sell")   
                    else:
                                            print("kijun et chikou sell")   
                else:
                                            print("tenkan et chikou sell")                                                                                                                  
            else:
                print("close et chikou sell")
        else:
             print("nonon")                                        
                                               
        if len(mt5.positions_get(symbol=self.symbol)) != 0:
            print("mt5.positions_get(symbol=self.symbol)[0].type ",mt5.positions_get(symbol=self.symbol)[0].type)
            if(( mt5.positions_get(symbol=self.symbol)[0].type==0 and self.ask>= self.close_threshold_val_buy and round( ichimoku_df['chikou_span'][200-27],4)>round( ichimoku_df["kijun_sen"][200-27],4) and round( ichimoku_df['low'][199],4)<=round( ichimoku_df["tenkan_sen"][199],4) and round( ichimoku_df['high'][199],4)>=round( ichimoku_df["tenkan_sen"][199],4) and round( ichimoku_df['close'][199],4)<round( ichimoku_df['open'][199] ,4))or ( mt5.positions_get(symbol=self.symbol)[0].type==0  and round( ichimoku_df['chikou_span'][200-27],4)<=round( ichimoku_df['kijun_sen'][200-27],4) )):
               print("le bid est ",self.ask)
               print("l close thresholf ",self.close_threshold_val_buy )
               decision="close_long"
               print("we will close long position")
               return decision
              
        if len(mt5.positions_get(symbol=self.symbol)) != 0:
            if(( mt5.positions_get(symbol=self.symbol)[0].type==1 and self.bid<= self.close_threshold_val_sell and round( ichimoku_df['chikou_span'][200-27],4)<round( ichimoku_df["kijun_sen"][200-27],4) and round( ichimoku_df['low'][199],4)<=round( ichimoku_df["tenkan_sen"][199],4) and round( ichimoku_df['high'][199],4)>=round( ichimoku_df["tenkan_sen"][199],4)  and round( ichimoku_df['close'][199],4)>round( ichimoku_df['open'][199],4)  )or (mt5.positions_get(symbol=self.symbol)[0].type==1  and round( ichimoku_df['chikou_span'][200-27],4)>=round( ichimoku_df['kijun_sen'][200-27],4))):
                print("le bid est ",self.bid)
                print((mt5.positions_get(symbol=self.symbol)[0].type==1  and round( ichimoku_df['chikou_span'][200-27],4)>=round( ichimoku_df['kijun_sen'][200-27],4)))
                print("round( ichimoku_df['chikou_span'][200-27],4) ",round( ichimoku_df['chikou_span'][200-27],4))
                print("round( ichimoku_df['kijun_sen'][200-27],4)) ",round( ichimoku_df['kijun_sen'][200-27],4))
                print("l close threshol ",self.close_threshold_val_sell )
                decision="close_short"
                print("we will close short position")
                return decision
            else:
                print( "bid",self.bid)
            print((mt5.positions_get(symbol=self.symbol)[0].type==1  and round( ichimoku_df['chikou_span'][200-27],4)>=round( ichimoku_df['kijun_sen'][200-27],4)))
            print("round( ichimoku_df['chikou_span'][200-27],4) ",ichimoku_df['chikou_span'][200-27],4)
            print("round( ichimoku_df['kijun_sen'][200-27],4)) ", ichimoku_df['kijun_sen'][200-27],4) 
            
        
   