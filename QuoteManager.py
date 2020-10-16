import uuid
from datetime import date
import datetime
from abc import ABCMeta, abstractmethod


dic={}

class ABCQuote(object, metaclass=ABCMeta):
    def __init__(self, symbol: str, price: float, available_volume: int, expiration_datetime: datetime = None,
                 guid: uuid.UUID = None):
        self.guid = guid if guid else uuid.uuid4()
        self.symbol = symbol
        self.price = price
        self.available_volume = available_volume
        self.expiration_datetime = expiration_datetime

class Quote(ABCQuote):
    def __init__(self, symbol: str, price: float, available_volume: int, expiration_datetime: datetime = None,
                 guid: uuid.UUID = None):
        super().__init__(symbol, price, available_volume, expiration_datetime, guid)


class ABCTradeResult(object, metaclass=ABCMeta):
    def __init__(self, symbol: str, volume_weighted_average_price: float, volume_requested: int, volume_executed: int,
                 guid: uuid.UUID = None):
        self.guid = guid if guid else uuid.uuid4()
        self.symbol = symbol
        self.volume_weighted_average_price = volume_weighted_average_price
        self.volume_requested = volume_requested
        self.volume_executed = volume_executed


class TradeResult(ABCTradeResult):
    def __init__(self, symbol: str, volume_weighted_average_price: float, volume_requested: int, volume_executed: int,
                 guid: uuid.UUID = None):
        super().__init__(symbol, volume_weighted_average_price, volume_requested, volume_executed, guid)


class ABCQuoteManager(object, metaclass=ABCMeta):
    @abstractmethod
    def add_or_update_quote_by_guid(self, guid: uuid.UUID, abc_quote: ABCQuote):
        raise NotImplementedError()
    @abstractmethod
    def remove_quote(self, guid: uuid.UUID):
        raise NotImplementedError()
    @abstractmethod
    def remove_all_quotes(self, symbol: str):
        raise NotImplementedError()
    @abstractmethod
    def get_best_quote_with_available_volume(self, symbol: str) -> ABCQuote:
        raise NotImplementedError()
    @abstractmethod
    def execute_trade(self, symbol: str, volume_requested: int) -> ABCTradeResult:
        raise NotImplementedError()

class QuoteManager(ABCQuoteManager):
    def add_or_update_quote_by_guid(self, guid: uuid.UUID, abc_quote: ABCQuote):
      if guid in dic:
        print('The quote with same id exits. So Updating it to new value')
        dic[guid]=abc_quote
      else:
        dic[guid]=abc_quote
    
    
    def print_all(self):
      print("ID  SYM  PRICE     VOL  DATE")
      [print (i, "   ",dic[i].symbol,"   ",dic[i].price,"   ",dic[i].available_volume,"   ",dic[i].expiration_datetime) for i in dic]
      
        

    def remove_quote(self, guid: uuid.UUID):
      del dic[guid]


    def remove_all_quotes(self, symbol: str):
      #[del dic[key] for key in list(dic) if dic[key].symbol==symbol]

      for key in list(dic):
        #print(dic[key].symbol)
        if dic[key].symbol==symbol:
          del dic[key] 
 
    

    def get_best_quote_with_available_volume(self, symbol: str) -> ABCQuote:
      today = datetime.date.today()
      smallest= 1000000000000000000000000
      key=0
      for i in dic:
          if dic[i].expiration_datetime>today and smallest>dic[i].price and dic[i].available_volume:
            smallest=dic[i].price
            key=i
      print('smallest price is ',smallest)
      if smallest==0:
        return None
      return key


    def execute_trade(self, symbol: str, volume_requested: int) -> ABCTradeResult:
      pass
    

Quote1=Quote('A',100,20,date(2020, 4, 13))
Quote2=Quote('A',40,60,date(2020, 3, 21))
Quote3=Quote('B',120,720,date(2019, 12, 10))
Quote4=Quote('A',70,30,date(2020, 1, 12))
Quote5=Quote('E',70,30,date(2020, 7, 5))
Quote6=Quote('E',70,30,date(2020, 12, 4))
Quote7=Quote('E',20,0,date(2020, 12, 23))

TradeResult1=TradeResult('T1',100,20,30)
TradeResult2=TradeResult('T2',40,70,10)
TradeResult3=TradeResult('T3',10,10,70)
TradeResult4=TradeResult('T4',140,60,20)


QuoteManager1=QuoteManager()
QuoteManager1.add_or_update_quote_by_guid(1,Quote1)
QuoteManager1.add_or_update_quote_by_guid(2,Quote2)
QuoteManager1.add_or_update_quote_by_guid(3,Quote3)
QuoteManager1.add_or_update_quote_by_guid(4,Quote4)
QuoteManager1.add_or_update_quote_by_guid(5,Quote5)
QuoteManager1.add_or_update_quote_by_guid(6,Quote6)
QuoteManager1.add_or_update_quote_by_guid(7,Quote7)
QuoteManager1.print_all()


print("\n\n********************************* \n")
QuoteManager1.remove_all_quotes('E')
QuoteManager1.print_all()



print("\n\n********************************* \n")
price=QuoteManager1.get_best_quote_with_available_volume('E')
print(price)
