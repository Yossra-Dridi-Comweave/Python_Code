import MetaTrader5 as mt5
from Explorer import Explorer
from Decider import Decider
from Executor import Executor
from Orchestrator import Orchestrator
if __name__ == "__main__":
    symbol = "USDSGD"
    timeframe = mt5.TIMEFRAME_M5
    take_profit = 300
    
    lot_size = 0.10
  
    login=10002902151
    password="LuGsWe*2"
    server="MetaQuotes-Demo"
    explorer = Explorer(symbol, timeframe,login,password,server)
    
    decider = Decider(symbol, 0,0,0,0)
    executor = Executor(symbol ,lot_size,take_profit,50)

    orchestrateur = Orchestrator(explorer, decider, executor)
    orchestrateur.demarrer()
