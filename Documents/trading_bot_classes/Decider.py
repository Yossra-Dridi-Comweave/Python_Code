import MetaTrader5 as mt5
class Decider:
    def __init__(self, symbol, close_threshold_val_buy,close_threshold_val_sell):
         self.symbol=symbol
         
         self.close_threshold_val_buy=close_threshold_val_buy
         self.close_threshold_val_sell=close_threshold_val_sell
         
      
        
    def fetch_positions(self):
        return mt5.positions_get(symbol=self.symbol)  
    def check_buy_conditions(self, df,df1) :
        condition1_chikou_and_close_buy=df['chikou_span'][200-27]>df['close'][200-27]
        condition2_tenkan_chikou_buy=df['chikou_span'][200-27]>df['tenkan_sen'][200-27]
        condition3_kijun_chikou_buy=df['chikou_span'][200-27]>df['kijun_sen'][200-27]
        condition4_ssb_ssa_chikou_buy=df['chikou_span'][200-27]>df['senkou_span_b'][200-27] and df['chikou_span'][200-27]>df['senkou_span_a'][200-27]
        condition5_tenkan_kijun_buy=df['tenkan_sen'][199]>=df['kijun_sen'][199]
        condition6_ssb_kijun_buy=df['kijun_sen'][199]>df['senkou_span_b'][199] and df['kijun_sen'][199]>df['senkou_span_a'][199]
        condition7_close_open_buy=df['close'][199]>df['open'][199]
        condition8_tenkan_prix_buy=df['tenkan_sen'][199]<df['open'][199]
        
        
        condition11_prix_nuage_buy=df['low'][199]>df['senkou_span_b'][199] and df['low'][199]>df['senkou_span_a'][199] 
        #la condition finale d'ouverture d'une posiotn longue
        buy_condition= condition11_prix_nuage_buy and condition1_chikou_and_close_buy and condition8_tenkan_prix_buy and condition2_tenkan_chikou_buy and condition3_kijun_chikou_buy and condition4_ssb_ssa_chikou_buy and condition5_tenkan_kijun_buy and condition6_ssb_kijun_buy and condition7_close_open_buy
        
        print("condition1 chikou et close buy ",condition1_chikou_and_close_buy)
        print("condition2 tenkan et close buy ",condition2_tenkan_chikou_buy)
        print("condition3 kijun et chikou buy ",condition3_kijun_chikou_buy)
        print("condition4 buy ssb et chikou ",condition4_ssb_ssa_chikou_buy)
        print("condition5 buy tenkan et kijun ",condition5_tenkan_kijun_buy)
        print("condition6 buy ssb et kijun ",condition6_ssb_kijun_buy)
        print("condition7 buy close et open ",condition7_close_open_buy)
        print("condition8_tenkan_prix_buy",condition8_tenkan_prix_buy)
        
        print("condition11_prix_nuage_buy ",condition11_prix_nuage_buy)
      
       
        #verfication des condiotions d'achat et execution du requete si les conditions sont verifiées
            


        condition1_chikou_and_close_buy_df1=df1['chikou_span'][200-27]>df1['close'][200-27]
        condition2_tenkan_chikou_buy_df1=df1['chikou_span'][200-27]>df1['tenkan_sen'][200-27]
        condition3_kijun_chikou_buy_df1=df1['chikou_span'][200-27]>df1['kijun_sen'][200-27]
        condition4_ssb_ssa_chikou_buy_df1=df1['chikou_span'][200-27]>df1['senkou_span_b'][200-27] and df1['chikou_span'][200-27]>df1['senkou_span_a'][200-27]
        condition5_tenkan_kijun_buy_df1=df1['tenkan_sen'][199]>df1['kijun_sen'][199]
        condition6_ssb_kijun_buy_df1=df1['kijun_sen'][199]>df1['senkou_span_b'][199]
        
        condition8_tenkan_prix_buy_df1=df1['tenkan_sen'][199]<df1['low'][199]
        condition11_prix_nuage_buy_df1=df1['low'][199]>df1['senkou_span_b'][199] and df1['low'][199]>df1['senkou_span_a'][199] 
    
        buy_condition_df1=  condition1_chikou_and_close_buy_df1 and  condition2_tenkan_chikou_buy_df1 and condition3_kijun_chikou_buy_df1 and condition4_ssb_ssa_chikou_buy_df1 and condition5_tenkan_kijun_buy_df1 and condition6_ssb_kijun_buy_df1 and condition8_tenkan_prix_buy_df1 and condition11_prix_nuage_buy_df1 
        print("buy_condition_df1 ",buy_condition_df1)
        return buy_condition
    def check_sell_conditions(self,df,df1):
        condition1_chikou_and_close_sell=df['close'][200-27]>df['chikou_span'][200-27]
        condition2_chikou_tenkan_sell=df['chikou_span'][200-27]<df['tenkan_sen'][200-27]
        condition3_kijun_chikou_sell=df['chikou_span'][200-27]<df['kijun_sen'][200-27]
        condition4_ssb_chikou_sell=df['chikou_span'][200-27]<df['senkou_span_b'][200-27] and df['chikou_span'][200-27]<df['senkou_span_a'][200-27]
        
        condition8_prix_tenkan=df["tenkan_sen"][199] > df['close'][199]
        condition5_tenkan_kijun_sell=df['tenkan_sen'][199]<=df['kijun_sen'][199]
        condition11_prix_nuage_sell=df['high'][199]<df['senkou_span_b'][199] and df['high'][199]<df['senkou_span_a'][199] 
        condition6_ssb_kijun_sell=df['kijun_sen'][199]<df['senkou_span_b'][199] and df['kijun_sen'][199]<df['senkou_span_a'][199] 
        condition7_close_open_sell=df['close'][199]<df['open'][199]
        print("condition1 chikou et close ",condition1_chikou_and_close_sell)
        print("condition2 tenkan et close ",condition2_chikou_tenkan_sell)
        print("condition3 kijun et chikou ",condition3_kijun_chikou_sell)
        print("condition4 ssb et chikou",condition4_ssb_chikou_sell)
        print("condition5 tenkanet kijun ",condition5_tenkan_kijun_sell)
        print("condition8_prix_tenkan ",condition8_prix_tenkan)
        print("condition6 ssb et kijun ",condition6_ssb_kijun_sell)
        print("kijun ",df['kijun_sen'][199])
        print("ssb ",df['senkou_span_b'][199])
        print("condition7 open et close",condition7_close_open_sell)
    
        print(" condition11_prix_nuage_sell ", condition11_prix_nuage_sell)
       
        
        
        
        #Condition finale pour ouvrir une position courte
        sell_condition=condition8_prix_tenkan  and condition1_chikou_and_close_sell and  condition11_prix_nuage_sell and condition2_chikou_tenkan_sell and condition3_kijun_chikou_sell and condition4_ssb_chikou_sell and condition5_tenkan_kijun_sell and condition6_ssb_kijun_sell  and condition7_close_open_sell
        condition1_chikou_and_close_sell_df1=df1['close'][200-27]>df1['chikou_span'][200-27]
        condition2_chikou_tenkan_sell_df1=df1['chikou_span'][200-27]<df1['tenkan_sen'][200-27]
        condition3_kijun_chikou_sell_df1=df1['chikou_span'][200-27]<df1['kijun_sen'][200-27]
        condition4_ssb_chikou_sell_df1=df1['chikou_span'][200-27]<df1['senkou_span_b'][200-27] and df1['chikou_span'][200-27]<df1['senkou_span_a'][200-27]
        condition8_prix_tenkan_df1=df1["tenkan_sen"][199] > df1['high'][199]
        condition5_tenkan_kijun_sell_df1=df1['tenkan_sen'][199]<df1['kijun_sen'][199]
        condition11_prix_nuage_sell_df1=df1['high'][199]<df1['senkou_span_b'][199] and df1['high'][199]<df1['senkou_span_a'][199] 
        condition6_ssb_kijun_sell_df1=df1['kijun_sen'][199]<df1['senkou_span_b'][199]
       
       
        sell_condition_df1= condition1_chikou_and_close_sell_df1  and condition2_chikou_tenkan_sell_df1 and condition3_kijun_chikou_sell_df1 and condition4_ssb_chikou_sell_df1 and condition8_prix_tenkan_df1 and condition5_tenkan_kijun_sell_df1 and condition11_prix_nuage_sell_df1 and condition6_ssb_kijun_sell_df1
        return sell_condition and sell_condition_df1
    def check_close_sell_conditions(self,ichimoku_df):  
        positions = mt5.positions_get(symbol=self.symbol)

   
        if not positions:
           return False 
        else:
            close_sell_position_conditions=(mt5.positions_get(symbol= self.symbol)[0].type== 1 and mt5.symbol_info_tick(self.symbol).bid<= self.close_threshold_val_sell and 
            ichimoku_df['chikou_span'][173] < ichimoku_df["kijun_sen"][173]  and
            ichimoku_df['open'][199] <= ichimoku_df["tenkan_sen"][199]  and
            ichimoku_df['close'][199] >= ichimoku_df["tenkan_sen"][199]  and
            ichimoku_df['close'][199] > ichimoku_df['open'][199] 
            ) or  (mt5.positions_get(symbol= self.symbol)[0].type== 1 and ichimoku_df['chikou_span'][173]  >= ichimoku_df['kijun_sen'][173] ) or( mt5.positions_get(symbol= self.symbol)[0].type== 1 and ichimoku_df['tenkan_sen'][199] > ichimoku_df["kijun_sen"][199])
                
            return close_sell_position_conditions
    
    def check_close_buy_conditions(self,df):  
        positions = mt5.positions_get(symbol=self.symbol)

   
        if not positions:
           return False 
        else:
            close_buy_position_conditions=( mt5.positions_get(symbol= self.symbol)[0].type==0 and  mt5.symbol_info_tick(self.symbol).ask>=  self.close_threshold_val_buy 
                                        and round(df['chikou_span'][173],4)>round(df["kijun_sen"][173],4) and round(df['close'][199],4)<=round(df["tenkan_sen"][199],4) 
                                        and round(df['open'][199],4)>=round(df["tenkan_sen"][199],4) and round(df['close'][199],4)<round(df['open'][199] ,4))or ( mt5.positions_get(symbol= self.symbol)[0].type==0  and  df['chikou_span'][173]<=df['kijun_sen'][173] )or ( mt5.positions_get(symbol= self.symbol)[0].type==0  and df['tenkan_sen'][199] < df["kijun_sen"][199])
            return close_buy_position_conditions
    def decide(self, ichimoku_df,df1):
        buy_condition = self.check_buy_conditions(ichimoku_df,df1)
        sell_condition = self.check_sell_conditions(ichimoku_df,df1)
        close_buy_condition = self.check_close_buy_conditions(ichimoku_df)
        close_sell_condition = self.check_close_sell_conditions(ichimoku_df)
        current_positions = self.fetch_positions()

        if len(current_positions) == 0:
            if buy_condition:
                return "buy"
            elif sell_condition: 
                return "sell"
        elif current_positions:
            positions = self.fetch_positions()
            print("il ay ddes posiotns ")
 
            if positions:
             first_position_profit = positions[0].profit
             print( "first_position_profit ", first_position_profit)
             if (close_buy_condition or first_position_profit<-5) and positions[0].type==0 :
                print("close_buy")
                return "close_buy"
             elif ( close_sell_condition or first_position_profit<-5) and positions[0].type==1:
                return "close_sell"  
             elif(first_position_profit>0):
                           return "deplacer_sl"
                                               

        return "no action"
  
