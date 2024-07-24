import MetaTrader5 as mt5
from Explorer import Explorer
from Decider import Decider
from Executor import Executor
from Orchestrator import Orchestrator

def start_trading(symbol,timeframe,take_profit,lot_size,login,password,server):
   
    explorer = Explorer(symbol, timeframe, login, password, server)
    print("symbol,timeframe,take_profit,lot_size,login,password,server " ,symbol,timeframe,take_profit,lot_size,login,password,server)
    decider = Decider(symbol, 0, 0)
    executor = Executor(symbol, lot_size,take_profit, 100,0)
    orchestrator = Orchestrator(explorer, decider, executor, timeframe)
    orchestrator.demarrer()
