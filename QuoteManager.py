import uuid
from datetime import date
import datetime
from abc import ABCMeta, abstractmethod


Quote_dic={}
Trade_dic={}

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
    def get_best_quote_with_available_volume(self, symbol: str) -> ABCQuote:
        raise NotImplementedError()
    @abstractmethod
    def execute_Trade_dic(self, symbol: str, volume_requested: int) -> ABCTradeResult:
        raise NotImplementedError()






class QuoteManager(ABCQuoteManager):

    def add_or_update_quote_by_guid(self, guid: uuid.UUID, abc_quote: ABCQuote):
      if guid in Quote_dic:
        print('\n\t The quote with same id exits. So updating it to new value')
        Quote_dic[guid].symbol=abc_quote.symbol
        Quote_dic[guid].price=abc_quote.price
        Quote_dic[guid].available_volume=abc_quote.available_volume
        Quote_dic[guid].expiration_datetime=abc_quote.expiration_datetime
      else:
        Quote_dic[guid]=abc_quote

      print('Successfully added ',abc_quote.symbol,'into the Quote_dic ' )



    def remove_quote(self, guid: uuid.UUID):
      del Quote_dic[guid]


    def remove_all_quotes(self, symbol: str):
      for key in list(Quote_dic):
        if Quote_dic[key].symbol==symbol:
          del Quote_dic[key] 
      print('\n Removed all quotes of',symbol)
      self.print_all_Quote_dic()

 
 
    def get_best_quote_with_available_volume(self, symbol: str,exclude=[]) -> ABCQuote:
      # id's in the exclude list will be ignored. This is required inside the execute_Trade_dic_recursion()  to find the next smallest element 
      today = datetime.date.today()
      smallest= 1000000000000000000000000
      key=0
      for i in Quote_dic:
          if Quote_dic[i].symbol==symbol and Quote_dic[i].expiration_datetime>today and smallest>Quote_dic[i].price and Quote_dic[i].available_volume and Quote_dic[i].guid not in exclude:
            smallest=Quote_dic[i].price
            key=i
      if smallest==1000000000000000000000000:
        print('\nNo quote is available' )
        return None
      print('\nThe best quote for symbol',symbol,'is ',smallest )
      return key




    def execute_Trade_dic(self, symbol: str, volume_requested: int) -> ABCTradeResult:
      exclude=[]
      result=volume_requested
      global_volume_requested=volume_requested
      i=1
      if self.get_best_quote_with_available_volume(symbol,exclude):
        while result>=0 :
          print('\n\n\t\t\t * Entered execeute Trade_dic :',i,'* \n')
          result=self.execute_Trade_dic_recursion(symbol, result,global_volume_requested,exclude)
          print('RESULT/REMAINING VOL = ',result)
          i+=1
        print("\n\n\n-----------------------------------------------------------------------------")
        print("\n\n\t\t\t\t FINAL QUOTE TABLE\n\n")
        self.print_all_Quote_dic()
      else:
        print('\nERROR \t No quote is available')


    def execute_Trade_dic_recursion(self, symbol: str, volume_requested: int,global_volume_requested:int, exclude) -> ABCTradeResult:
      lowest_price_id=self.get_best_quote_with_available_volume(symbol,exclude)
      print('The id of symbol', symbol,'with lowest price : ',lowest_price_id)
      if lowest_price_id:
        diff_btw_requested_and_available=Quote_dic[lowest_price_id].available_volume-volume_requested
        print('the diff is ', diff_btw_requested_and_available)

        if diff_btw_requested_and_available>=0:
          Quote_dic[lowest_price_id].available_volume-=volume_requested        
          id=uuid.uuid4()
          Trade_dic[id]= TradeResult(symbol,Quote_dic[lowest_price_id].price,global_volume_requested,volume_requested)
          return -1
        else:
          remaining_vol=volume_requested-Quote_dic[lowest_price_id].available_volume
          volume_requested-=Quote_dic[lowest_price_id].available_volume
          volume_executed=Quote_dic[lowest_price_id].available_volume
          
          Quote_dic[lowest_price_id].available_volume-=Quote_dic[lowest_price_id].available_volume
          exclude.append(lowest_price_id)
          id=uuid.uuid4()
          Trade_dic[id]= TradeResult(symbol,Quote_dic[lowest_price_id].price,global_volume_requested,volume_executed)
          return remaining_vol
        
      else:
        print('ERROR OCCURED \n ')
        return 'error'

    
    
    
    def print_all_Quote_dic(self):
      print("\n\n\t\t%%%%%%%%%%%%% Displaying Quote_dic %%%%%%%%%%%%%n")
      print("ID  |    SYM    |    PRICE     |   Available Vol  |        DATE")
      [print (i, " \t\t",Quote_dic[i].symbol," \t\t",Quote_dic[i].price," \t\t\t",Quote_dic[i].available_volume," \t\t\t",Quote_dic[i].expiration_datetime) for i in Quote_dic]

 


    def print_all_Trade_dic(self):
        print("\n\n\t\t%%%%%%%%%%%%% Displaying Trade_dic Quote_dic %%%%%%%%%%%%%")
        print("SYM | vol/wt | vol_req | vol_exec")
        [print (Trade_dic[i].symbol,"   ",Trade_dic[i].volume_weighted_average_price,"   ",Trade_dic[i].volume_requested,"    ",Trade_dic[i].volume_executed) for i in Trade_dic]





Quote1=Quote('A',1,750,date(2020, 12, 13))
Quote2=Quote('A',2,1000,date(2020, 12, 21))
Quote3=Quote('B',120,720,date(2020, 12, 10))
Quote4=Quote('A',70,30,date(2019, 1, 12))
Quote5=Quote('E',70,30,date(2020, 7, 5))
Quote6=Quote('E',70,30,date(2020, 12, 4))
Quote7=Quote('C',30,30,date(2020, 12, 10))
Quote8=Quote('C',10,10,date(2020, 12, 13))
Quote9=Quote('C',20,20,date(2020, 12, 21))


QuoteManager1=QuoteManager()
QuoteManager1.add_or_update_quote_by_guid(1,Quote1)
QuoteManager1.add_or_update_quote_by_guid(2,Quote2)
QuoteManager1.add_or_update_quote_by_guid(3,Quote3)
QuoteManager1.add_or_update_quote_by_guid(4,Quote4)
QuoteManager1.add_or_update_quote_by_guid(5,Quote5)
QuoteManager1.add_or_update_quote_by_guid(6,Quote6)
QuoteManager1.add_or_update_quote_by_guid(7,Quote7)
QuoteManager1.add_or_update_quote_by_guid(8,Quote8)
QuoteManager1.add_or_update_quote_by_guid(9,Quote9)

print("\n\n\n-----------------------------------------------------------------------------")
print("\n\n\t\t\t\t INITIAL QUOTE TABLE  \n")
QuoteManager1.print_all_Quote_dic()

#QuoteManager1.remove_all_quotes('A')
#QuoteManager1.remove_all_quotes('B')
#QuoteManager1.get_best_quote_with_available_volume('C')


#print("\n\n********************************* \n")
#QuoteManager1.execute_Trade_dic('A',500)
#QuoteManager1.execute_Trade_dic('A',500)

