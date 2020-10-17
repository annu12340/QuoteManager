import pytest
from ToDeleteQuoteManager import *

QuoteManager1 = QuoteManager()

def test_for_Empty_Symbol():
    with pytest.raises(KeyError):
     assert QuoteManager1.remove_quote('') == KeyError('Key is not found')
     assert QuoteManager1.remove_all_quotes('') == KeyError('Symbol is not found')
     assert QuoteManager1.get_best_quote_with_available_volume('') == None
     assert QuoteManager1.execute_Trade('', 100) == None

def test_for_NonExistent_Symbol():
    with pytest.raises(KeyError):
     assert QuoteManager1.remove_all_quotes('Non existent symbol') == KeyError('Symbol is not found')
     assert QuoteManager1.remove_quote(123456789) == KeyError('Key is not found')
     assert QuoteManager1.get_best_quote_with_available_volume('Non existent symbol') == None
     assert QuoteManager1.execute_Trade('Non existent symbol', 100) == None

def test_for_Existing_Symbol():
    with pytest.raises(KeyError):
     assert QuoteManager1.remove_all_quotes('A') != KeyError('Symbol is not found')
     assert QuoteManager1.remove_quote('6699e7d4-32c7-498d-b4c4-7391cb435735') != KeyError('Key is not found')
     assert QuoteManager1.get_best_quote_with_available_volume('A') != None
     assert QuoteManager1.execute_Trade('A', 1) != None

def test_for_special_cases():
    QuoteManager1.add_or_update_quote_by_guid(0, Quote("smallest_symbol", 0, 10, date(2020, 12, 21)))
    QuoteManager1.add_or_update_quote_by_guid(-1, Quote("symbol with expiry date on 2019", 50, 50, date(2019, 12, 21)))
    assert QuoteManager1.get_best_quote_with_available_volume("smallest_symbol") == 0
    assert QuoteManager1.execute_Trade("smallest_symbol",900) == None
    assert QuoteManager1.get_best_quote_with_available_volume("symbol with expiry date on 2019")==None
