import datetime
import uuid
from abc import ABCMeta, abstractmethod
from datetime import date

Quote_dic = {}
Trade_dic = {}


# ---------------------------------------------- ABCQuote ----------------------------------------------
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


# ---------------------------------------------- ABCTradeResult ----------------------------------------------
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


# ---------------------------------------------- ABCQuoteManager ----------------------------------------------
class ABCQuoteManager(object, metaclass=ABCMeta):
    @abstractmethod
    def add_or_update_quote_by_guid(self, guid: uuid.UUID, abc_quote: ABCQuote):
        raise NotImplementedError()

    @abstractmethod
    def remove_quote(self,symbol:str, guid: uuid.UUID):
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
      if abc_quote.symbol in Quote_dic:
        is_duplicate_id_present = False
        symbol_list= Quote_dic[abc_quote.symbol]
        
        # To check if same id exists in the dictionary. 
        for position_of_duplicate in range(len(symbol_list) ):
          if symbol_list[position_of_duplicate]['id']==guid:
            is_duplicate_id_present=True
            break

        if is_duplicate_id_present:
           print('\n\t The quote with same id exits. So updating it to new value')
           Quote_dic[ abc_quote.symbol][position_of_duplicate].update({'id':guid, 'price': abc_quote.price,'available_volume':abc_quote.available_volume, 'expiration_datetime':abc_quote.expiration_datetime})
        else:
         Quote_dic[ abc_quote.symbol].append({'id':guid, 'price': abc_quote.price,'available_volume':abc_quote.available_volume, 'expiration_datetime':abc_quote.expiration_datetime})  

      else:
        print('Creating a new key-value pair for symbol',abc_quote.symbol)
        Quote_dic[ abc_quote.symbol]=[{'id':guid, 'price': abc_quote.price,'available_volume':abc_quote.available_volume, 'expiration_datetime':abc_quote.expiration_datetime}]


        
        

    def remove_quote(self, guid: uuid.UUID,symbol:str):
      Quote_dic[symbol]=list(filter(lambda x: x['id'] != guid, Quote_dic[symbol])) 

 
            


    def remove_all_quotes(self, symbol: str):
        del Quote_dic[symbol] 




    def get_best_quote_with_available_volume(self, symbol: str) -> ABCQuote:
      # Sort the list based on the value of price
      Quote_dic[symbol].sort(key=lambda x: x.get('price'))
      for position in range(len(Quote_dic[symbol])):
        if Quote_dic[symbol][position]['expiration_datetime'] > datetime.date.today() and Quote_dic[symbol][position]['available_volume']:
            print('\nThe best quote for symbol',symbol,'is ',Quote_dic[symbol][position]['price'] )
            return position,Quote_dic[symbol][position]
      print('\n No quote is available')
      return None
    
      

        
        
    def execute_trade(self, symbol: str, volume_requested: int) -> ABCTradeResult:
      print("\n\n\n --------- Executing trade of ",symbol," volume requested : ",volume_requested,"-------  ")
      while True:
        position, quote = self.get_best_quote_with_available_volume(symbol)
        id = uuid.uuid4()
        
        if quote is None:
                return False

        elif quote['available_volume'] >= volume_requested:
                Quote_dic[symbol][position]['available_volume'] -= volume_requested
                Trade_dic[id] = TradeResult(symbol, quote['price'], volume_requested, volume_requested)
                return False
  
        else:
                volume_executed = quote['available_volume']
                Quote_dic[symbol][position]['available_volume']= 0
                Trade_dic[id] = TradeResult(symbol, quote['price'], volume_requested, volume_executed)
                return self.execute_trade(symbol,volume_requested - volume_executed)
      
      




    # --------------------- Display functions --------------------

    def print_all_Quote_dic(self):
        print("\n\n\t\t\t\t -----** Displaying Quote_dic **------\n")
        for i in Quote_dic:
          print('\n\n\n\t *** Symbol is',i,"*** \n" )
          print("ID    |  PRICE |  Available Vol |      DATE")
          [print(Quote_dic[i][j]['id'], " \t\t", Quote_dic[i][j]['price'], " \t\t", Quote_dic[i][j]['available_volume']," \t\t\t", Quote_dic[i][j]['expiration_datetime'] ) for j in range(len(Quote_dic[i]))]
            


        
    def print_all_Trade_dic(self):
        print("\n\n\t\t **-------- Displaying Trade_dic --------** \n")
        print("SYM |  vol/wt   | vol_req   |   vol_exec")
        [print(Trade_dic[i].symbol, "     ", Trade_dic[i].volume_weighted_average_price, "         ",
               Trade_dic[i].volume_requested, "        ", Trade_dic[i].volume_executed) for i in Trade_dic]
        

        
        
        
        

        
# ------------------------------------------------ * Object creation * ----------------------------------------------------------


QuoteManager1 = QuoteManager()
QuoteManager1.add_or_update_quote_by_guid(1, Quote('A', 50, 10, date(2020, 12, 13)))
QuoteManager1.add_or_update_quote_by_guid(2, Quote('A', 40, 20, date(2020, 12, 21)))
QuoteManager1.add_or_update_quote_by_guid(3, Quote('A', 30, 30, date(2020, 12, 10)))
QuoteManager1.add_or_update_quote_by_guid(4, Quote('B', 30, 30, date(2020, 11, 12)))
QuoteManager1.add_or_update_quote_by_guid(5, Quote('D', 440, 430, date(1999, 11, 12)))
QuoteManager1.add_or_update_quote_by_guid(6, Quote('A', 5, 750, date(2021, 11, 12)))
QuoteManager1.add_or_update_quote_by_guid(7, Quote('A', 10, 1000, date(2020, 12, 13)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('B', 20, 1000, date(2020, 12, 21)))
#QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('C', 30, 30, date(2020, 12, 10)))
#QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('E', 70, 30, date(2020, 7, 5)))
#QuoteManager1.add_or_update_quote_by_guid(8, Quote('E', 70, 30, date(2020, 12, 4)))
QuoteManager1.print_all_Quote_dic()

#QuoteManager1.remove_all_quotes('A')
#QuoteManager1.remove_quote(3,'A')
#QuoteManager1.remove_quote(5,'C')
#QuoteManager1.print_all_Quote_dic()
#QuoteManager1.get_best_quote_with_available_volume('A')
#QuoteManager1.execute_trade('A',35)

QuoteManager1.execute_trade('A',500)
QuoteManager1.execute_trade('A',500)
QuoteManager1.print_all_Quote_dic()
