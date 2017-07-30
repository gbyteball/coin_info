from flask import Flask, render_template, request
import sqlalchemy
from db_example import show_tables
from api import getBitcoinPrice, getBittrexPrice, getCoinonePrice, getUSDKRW
from gevent.wsgi import WSGIServer
from collections import defaultdict
from bittrex.bittrex import Bittrex


app = Flask(__name__)
  
@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/sql')
def sql():
  return 'sql version : ' + sqlalchemy.__version__




@app.route('/coin')
def coin():
  result = show_tables()

  bittrexCoinList = ['ETH', 'XRP', 'PAY', 'GBYTE', 'EDG', 'SNT', 'ADX', 'OMG', 'DASH', 'ZEC', 'GNT', 'NXT', 'STRAT', 'QTUM', 'KMD', 'NMR']

  for coindict in result:
    if bittrexCoinList.count(coindict['code']) == 1:
      coindict['coin_price'] = getBittrexPrice('BTC', coindict['code'], 'Last')
    elif coindict['code'] == 'BTC':
      coindict['coin_price'] = getBitcoinPrice()
    elif coindict['code'] == 'USD':
      coindict['coin_price'] = getUSDKRW()
    else:
      coindict['coin_price'] = 0


# profit_percent
# profit_value
# price_now
# 10kKRW_coin_amount
# asset_rate


  bPrice = Bittrex()
  print(Bittrex.get_balances(bPrice))



  pUSD = getUSDKRW()
  pBTC = getBitcoinPrice()
  pETH = getBittrexPrice('BTC', 'ETH', 'Last')
  pXRP = getBittrexPrice('BTC', 'XRP', 'Last')

  pBTCWon = getCoinonePrice('BTC')
  if pBTCWon == 0:
    pBTCWon = pUSD*pBTC
    pETHWon = pUSD*pETH*pBTC
    pXRPWon = pUSD*pXRP*pBTC
  else:
    pETHWon = getCoinonePrice('ETH')
    if pETHWon == 0:
      pETHWon = pUSD*pETH*pBTC
      pXRPWon = pUSD*pXRP*pBTC
    pXRPWon = getCoinonePrice('XRP')
    if pXRPWon == 0:
      pXRPWon = pUSD*pXRP*pBTC

  total_price_init = sum([i['price_init'] for i in result])
  refreshSec = request.args.get('refresh')
  
  return render_template('coin.html', result = result, pUSD = pUSD, pBTC = pBTC, pBTCWon = pBTCWon, pETH = pETH, pETHWon = pETHWon, pXRP = pXRP, pXRPWon = pXRPWon, total_price_init = total_price_init, refreshSec = refreshSec)




if __name__ == '__main__':
  app.debug=True
#  app.run(host='0.0.0.0')
  http_server = WSGIServer(('0.0.0.0', 5000), app)
  http_server.serve_forever()