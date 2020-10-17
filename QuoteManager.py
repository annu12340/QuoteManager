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
    def remove_quote(self, guid: uuid.UUID):
        raise NotImplementedError()

    @abstractmethod
    def remove_all_quotes(self, symbol: str):
        raise NotImplementedError()

    @abstractmethod
    def get_best_quote_with_available_volume(self, symbol: str) -> ABCQuote:
        raise NotImplementedError()

    @abstractmethod
    def execute_Trade(self, symbol: str, volume_requested: int) -> ABCTradeResult:
        raise NotImplementedError()






class QuoteManager(ABCQuoteManager):

    def add_or_update_quote_by_guid(self, guid: uuid.UUID, abc_quote: ABCQuote):
        if guid in Quote_dic:
            print('\n\t The quote with same id exits. So updating it to new value')
            Quote_dic[guid].symbol = abc_quote.symbol
            Quote_dic[guid].price = abc_quote.price
            Quote_dic[guid].available_volume = abc_quote.available_volume
            Quote_dic[guid].expiration_datetime = abc_quote.expiration_datetime
        else:
            Quote_dic[guid] = abc_quote
        print('Successfully added ', abc_quote.symbol, 'into the Quote_dic ')



    def remove_quote(self, guid: uuid.UUID):
        if guid in Quote_dic:
            del Quote_dic[guid]
        else:
            raise KeyError('Key is not found')



    def remove_all_quotes(self, symbol: str):
        symbol_found = 0
        if symbol:
            for key in list(Quote_dic):
                if Quote_dic[key].symbol == symbol:
                    del Quote_dic[key]
                    symbol_found = 1
            print('\n Removed all quotes of', symbol)
            self.print_all_Quote_dic()
            if symbol_found == 0:
                raise KeyError('Symbol is not found')
        else:
            raise KeyError('Symbol is not found')




    def get_best_quote_with_available_volume(self, symbol: str) -> ABCQuote:
      today = datetime.date.today()
      smallest_value= 1000000
      smallest_key_id=-1
      for i in Quote_dic:
          if Quote_dic[i].symbol==symbol and Quote_dic[i].expiration_datetime>today and smallest_value>Quote_dic[i].price and Quote_dic[i].available_volume:
            smallest_value=Quote_dic[i].price
            smallest_key_id=i

      if smallest_value==1000000:
        print('\nNo quote is available' )
        return None
      print('\nThe best quote for symbol',symbol,'is ',smallest_value )
      return smallest_key_id





    def execute_Trade(self, symbol: str, volume_requested: int) -> ABCTradeResult:
        result = volume_requested
        global_volume_requested = volume_requested
        no_of_iteration = 1

        if self.get_best_quote_with_available_volume(symbol):
            while result >= 0:
                print('\n\n\t\t\t * No of iteration:', no_of_iteration, '*')
                result = self.execute_Trade_recursion(symbol, result, global_volume_requested)
                print('REMAINING VOL = ', result)
                no_of_iteration += 1
            self.print_all_Trade_dic()
            self.print_all_Quote_dic()
        else:
            print('\nERROR \t No quote is available')




    def execute_Trade_recursion(self, symbol: str, volume_requested: int, global_volume_requested: int,) -> ABCTradeResult:
        lowest_price_id = self.get_best_quote_with_available_volume(symbol)
        if lowest_price_id:
            diff_btw_requested_and_available = Quote_dic[lowest_price_id].available_volume - volume_requested
            print('the diff is ', diff_btw_requested_and_available)

            if diff_btw_requested_and_available >= 0:
                #If diff is positive, then reduce its avialabilty in Quote_dic and add it into the Trade_dic. This would stop the recursion call

                Quote_dic[lowest_price_id].available_volume -= volume_requested
                id = uuid.uuid4()
                Trade_dic[id] = TradeResult(symbol, Quote_dic[lowest_price_id].price, global_volume_requested, volume_requested)
                return -1
            else:
                # If diff is negative, it means that the available vol of lowest price symbol is not sufficient. So we need to find the next lowest price symbol
                volume_requested -= Quote_dic[lowest_price_id].available_volume

                Quote_dic[lowest_price_id].available_volume -= Quote_dic[lowest_price_id].available_volume
                id = uuid.uuid4()
                Trade_dic[id] = TradeResult(symbol, Quote_dic[lowest_price_id].price, global_volume_requested, Quote_dic[lowest_price_id].available_volume)
                # volume_requested will be the remaining vol
                # ie remaining_vol = volume_requested - Quote_dic[lowest_price_id].available_volume
                return volume_requested
        else:
            print('ERROR OCCURED \n ')
            return -1

    # --------------------- Display functions --------------------

    def print_all_Quote_dic(self):
        print("\n\n\t\t --------** Displaying Quote_dic **---------\n")
        print(" \t\t\t    ID  \t\t\t\t\t   |    SYM    |    PRICE     |   Available Vol  |        DATE")
        [print(i, " \t\t\t", Quote_dic[i].symbol, " \t\t", Quote_dic[i].price, " \t\t\t", Quote_dic[i].available_volume,
               " \t\t\t", Quote_dic[i].expiration_datetime) for i in Quote_dic]

    def print_all_Trade_dic(self):
        print("\n\n\t\t **-------- Displaying Trade_dic --------** \n")
        print("SYM |  vol/wt   | vol_req   |   vol_exec")
        [print(Trade_dic[i].symbol, "     ", Trade_dic[i].volume_weighted_average_price, "         ",
               Trade_dic[i].volume_requested, "        ", Trade_dic[i].volume_executed) for i in Trade_dic]


# ------------------------------------------------ * Object creation * ----------------------------------------------------------

QuoteManager1 = QuoteManager()
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('A', 10, 750, date(2020, 12, 13)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('A', 20, 1000, date(2020, 12, 21)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('B', 120, 720, date(2020, 12, 10)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('A', 30, 30, date(2020, 11, 12)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('E', 70, 30, date(2020, 7, 5)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('E', 70, 30, date(2020, 12, 4)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('C', 10, 10, date(2020, 12, 13)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('C', 20, 20, date(2020, 12, 21)))
QuoteManager1.add_or_update_quote_by_guid(uuid.uuid4(), Quote('C', 30, 30, date(2020, 12, 10)))



print("\n\t\t\t\t __________________________________ INITIAL QUOTE TABLE __________________________________ ")
QuoteManager1.print_all_Quote_dic()

# QuoteManager1.remove_all_quotes('A')
# QuoteManager1.remove_quote('96f85c32-38aa-4d3b-814a-ba8de8620e20')
# QuoteManager1.get_best_quote_with_available_volume('A')
# print("\n\n********************************* \n")
QuoteManager1.execute_Trade('A', 500)
QuoteManager1.execute_Trade('A', 500)
QuoteManager1.execute_Trade('C',35)
