
import binance


api_key = "WA57b7Xw7jhd5P1t78Z3gj6AuB8D9iSgbaZJEs16TjyJCfw2ds8mIUJdQDqmAVXG"
api_secret = "9m2mU7iWLWS2v0q2rgFzkdyGx3gSUIMi1n6Sx9ItBInWL1y7Cxl6Tf5A2AwTYzA7"


client = binance.Client(api_key, api_secret)

# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
print(btc_price)


# get market depth
depth = client.get_order_book(symbol='BNBBTC')

print(depth)

