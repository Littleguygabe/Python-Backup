import alpaca_trade_api as tradeapi

api = tradeapi.REST(
    key_id='PK8Q16R5N2ESCHJXACWE',
    secret_key='1oAkeBHiXMxQaKmsnBfefRf063p9FwvldZBw8FjJ',
    base_url='https://paper-api.alpaca.markets'
)

account = api.get_account()
#stores all account details


api.submit_order(
    symbol='NVDA',
    qty=1,
    side='sell',
    type='market',
    time_in_force='gtc'
)

positions = api.list_positions()

for p in positions:
    print(p)






