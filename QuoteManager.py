import uuid,datetime
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

# TradeResult('T1',100,20,30)
class ABCQuoteManager(object, metaclass=ABCMeta):

    # Add or update the quote (specified by Id) in symbol's book. 
    # If quote is new or no longer in the book, add it. Otherwise update it to match the given price, volume, and symbol.
    @abstractmethod
    def add_or_update_quote_by_guid(self, guid: uuid.UUID, abc_quote: ABCQuote):
        raise NotImplementedError()

    # Remove quote by Id, if quote is no longer in symbol's book do nothing.
    @abstractmethod
    def remove_quote(self, guid: uuid.UUID):
        raise NotImplementedError()

    # Remove all quotes on the specifed symbol's book.
    @abstractmethod
    def remove_all_quotes(self, symbol: str):
        raise NotImplementedError()

    # Get the best (i.e. lowest) price in the symbol's book that still has available volume.
    # If there is no quote on the symbol's book with available volume, return null.
    # Otherwise return a Quote object with all the fields set.
    # Don't return any quote which is past its expiration time, or has been removed.
    @abstractmethod
    def get_best_quote_with_available_volume(self, symbol: str) -> ABCQuote:
        raise NotImplementedError()

    # Request that a trade be executed. For the purposes of this interface, assume that the trade is a request to BUY, not sell. Do not trade an expired quotes.
    # To Execute a trade:
    # * Search available quotes of the specified symbol from best price to worst price.
    # * Until the requested volume has been filled, use as much available volume as necessary (up to what is available) from each quote, subtracting the used amount from the available amount.
    # For example, we have two quotes:
    # {Price: 1.0, Volume: 1,000, AvailableVolume: 750}
    # {Price: 2.0, Volume: 1,000, AvailableVolume: 1,000}
    # After calling once for 500 volume, the quotes are:
    # {Price: 1.0, Volume: 1,000, AvailableVolume: 250}
    # {Price: 2.0, Volume: 1,000, AvailableVolume: 1,000}
    # And After calling this a second time for 500 volume, the quotes are:
    # {Price: 1.0, Volume: 1,000, AvailableVolume: 0}
    # {Price: 2.0, Volume: 1,000, AvailableVolume: 750}
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
      for i in dic:
        print (i, dic[i].symbol,dic[i].price)

    def remove_quote(self, guid: uuid.UUID):
      del dic[guid]


    def remove_all_quotes(self, symbol: str):
      for key in list(dic):
        #print(dic[key].symbol)
        if dic[key].symbol==symbol:
          del dic[key] 

    

    def get_best_quote_with_available_volume(self, symbol: str) -> ABCQuote:
      pass
    def execute_trade(self, symbol: str, volume_requested: int) -> ABCTradeResult:
      pass
    

Quote1=Quote('A',100,20,datetime.datetime.now())
Quote2=Quote('A',40,60,datetime.datetime.now())
Quote3=Quote('B',120,720,datetime.datetime.now())
Quote4=Quote('A',70,30,datetime.datetime.now())
Quote5=Quote('E',70,30,datetime.datetime.now())
Quote6=Quote('E',70,30,datetime.datetime.now())
Quote7=Quote('E',70,30,datetime.datetime.now())

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
print("\n\n deleteing")
QuoteManager1.remove_all_quotes('E')
QuoteManager1.print_all()

