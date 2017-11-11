from flask import Flask, render_template, request
import sqlalchemy
from db_example import show_tables
from api import getBittrexPrice, getUSDKRW, getBittrexPrice2, getBitfinexPrice, getHitbtcPrice, getUSDKRW2
from bitfinex import getBitfinexBalances, getBitfinexBalance
from gevent.wsgi import WSGIServer
from collections import defaultdict
from bittrex.bittrex import Bittrex
import json
import multiprocessing
from multiprocessing import Process, Queue

app = Flask(__name__)
  
@app.route('/coin2')
def coin2():
  result = show_tables()


  pUSD = 0.0
  pBTC = 0.0
  pETH = 0.0
  pXRP = 0.0

  procs = []
  multiThreadResult = list()
  q = multiprocessing.Queue()

  # coin_price
  for coindict in result:
    if coindict['code'] == 'BTC':
      #p = multiprocessing.Process(target=getBittrexPrice2, args=('USDT', coindict['code'], 'Last', q))
      p = multiprocessing.Process(target=getBitfinexPrice, args=('USD', 'BTC', 'last_price', q))
      procs.append(p)
      p.start()
    elif coindict['code'] == 'USDT' or coindict['code'] == 'USD':
      #p = multiprocessing.Process(target=getUSDKRW2, args=('', q))
      #procs.append(p)
      #p.start()
      q.put([coindict['code'], 0])
    elif coindict['place'] == 'bittrex':
      p = multiprocessing.Process(target=getBittrexPrice2, args=('BTC', coindict['code'], 'Last', q))
      procs.append(p)
      p.start()
    elif coindict['place'] == 'bitfinex' or coindict['place'] == 'bitfinex_l':
      p = multiprocessing.Process(target=getBitfinexPrice, args=('BTC', coindict['code'], 'last_price', q))
      procs.append(p)
      p.start()
    elif coindict['code'] == 'BET':
      p = multiprocessing.Process(target=getHitbtcPrice, args=('ETH', coindict['code'], 'last', q))
      procs.append(p)
      p.start()
    else:
      q.put([coindict['code'], 0])
    
  for p in procs:
    p.join()

  while not q.empty():
    item = q.get()
#    print(item)
    for coindict in result:
      if coindict['code'] == item[0]:
        coindict['coin_price'] = item[1]
        if coindict['code'] == 'BTC':
          pBTC = coindict['coin_price']
        elif coindict['code'] == 'USDT':
          pUSD = coindict['satoshi']
          if(pUSD == 0):
	        pUSD = 0
        elif coindict['code'] == 'ETH':
          pETH = coindict['coin_price']
        elif coindict['code'] == 'XRP':
          pXRP = coindict['coin_price']
#        elif coindict['code'] == 'BET':
#          print(item[0])
#          print(item[1])


#  for coindict in result:    
##    coindict['coin_price'] = multiThreadResult[result.index(coindict)]
#    coindict['coin_price'] = q.get()[1]
##    print(q.get()[0])
##    print(coindict['coin_price'])
#    if coindict['code'] == 'BTC':
#      pBTC = coindict['coin_price']
#    elif coindict['code'] == 'USDT':
#      pUSD = coindict['coin_price']
#    elif coindict['code'] == 'ETH':
#      pETH = coindict['coin_price']
#    elif coindict['code'] == 'XRP':
#      pXRP = coindict['coin_price']

# price_now
# 10kKRW_coin_amount
# asset_rate


  bPrice = Bittrex()
  bittrexBalancesDict = Bittrex.get_balances(bPrice)
  if bittrexBalancesDict['success'] == True:
    for coindict in result:
      if coindict['place'] == 'bittrex':
        for h in bittrexBalancesDict['result']:
          if coindict['code'] == h['Currency'] and coindict['iswallet'] == 'N':
            coindict['amount'] = h['Balance']
#            print('amount reset : ', h['Currency'], h['Balance'])


  bitfinexBalancesDict = getBitfinexBalances()
  if(bitfinexBalancesDict is None):
    print('is null')
  else:
    for coindict in result:
      if coindict['place'] == 'bitfinex' and coindict['iswallet'] == 'N':
        coindict['amount'] = getBitfinexBalance(bitfinexBalancesDict, coindict['code'].lower(), 'exchange')
      elif coindict['place'] == 'bitfinex_l':
        coindict['amount'] = getBitfinexBalance(bitfinexBalancesDict, coindict['code'].lower(), 'lending')

#  pBTCWon = getCoinonePrice('BTC')
#  if pBTCWon == 0:
#    pBTCWon = pUSD*pBTC
#    pETHWon = pUSD*pETH*pBTC
#    pXRPWon = pUSD*pXRP*pBTC
#  else:
#    pETHWon = getCoinonePrice('ETH')
#    if pETHWon == 0:
#      pETHWon = pUSD*pETH*pBTC
#      pXRPWon = pUSD*pXRP*pBTC
#    pXRPWon = getCoinonePrice('XRP')
#    if pXRPWon == 0:
#      pXRPWon = pUSD*pXRP*pBTC
  pBTCWon = pUSD*pBTC
  pETHWon = pUSD*pETH*pBTC
  pXRPWon = pUSD*pXRP*pBTC


  # profit_percent
  for coindict in result:
    if coindict['amount'] != 0 and coindict['price_init'] != 0:
      if coindict['name'] == 'USD':
        coindict['profit_percent'] = ((pUSD * coindict['amount']) - coindict['price_init'])/coindict['price_init']*100
      elif coindict['name'] == 'KRW':
        coindict['profit_percent'] = ((1 * coindict['amount']) - coindict['price_init'])/coindict['price_init']*100
      elif coindict['name'] == 'Bitcoin':
        coindict['profit_percent'] = ((pBTCWon * coindict['amount']) - coindict['price_init'])/coindict['price_init']*100
      elif coindict['name'] == 'Ethereum':
        coindict['profit_percent'] = ((pETHWon * coindict['amount']) - coindict['price_init'])/coindict['price_init']*100
      elif coindict['name'] == 'Ripple':
        coindict['profit_percent'] = ((pXRPWon * coindict['amount']) - coindict['price_init'])/coindict['price_init']*100
      elif coindict['name'] == 'DAO.Casino':
	    coindict['profit_percent'] = ((coindict['coin_price']* coindict['amount'] * pETHWon) - coindict['price_init'])/coindict['price_init']*100
      elif coindict['name'] == 'BlackMoon':
	    coindict['profit_percent'] = ((coindict['satoshi']*0.00000001* coindict['amount'] * pETHWon) - coindict['price_init'])/coindict['price_init']*100
      elif coindict['name'] == 'Tezos' or coindict['name'] == 'Air':
        coindict['profit_percent'] = ((coindict['satoshi']*0.00000001* coindict['amount'] * pBTCWon) - coindict['price_init'])/coindict['price_init']*100
      else:
        coindict['profit_percent'] = ((coindict['coin_price'] * coindict['amount'] * pBTCWon) - coindict['price_init'])/coindict['price_init']*100
    else:
      coindict['profit_percent'] = 0


  # profit_value
  for coindict in result:
    if coindict['name'] == 'USD':
      coindict['profit_value'] = int((pUSD * coindict['amount']) - coindict['price_init'])
    elif coindict['name'] == 'KRW':
      coindict['profit_value'] = int((1 * coindict['amount']) - coindict['price_init'])
    elif coindict['name'] == 'Bitcoin':
      coindict['profit_value'] = int((pBTCWon * coindict['amount']) - coindict['price_init'])
    elif coindict['name'] == 'Ethereum':
      coindict['profit_value'] = int((pETHWon * coindict['amount']) - coindict['price_init'])
    elif coindict['name'] == 'Ripple':
      coindict['profit_value'] = int((pXRPWon * coindict['amount']) - coindict['price_init'])
    elif coindict['name'] == 'DAO.Casino':
      coindict['profit_value'] = int((coindict['coin_price'] * coindict['amount'] * pETHWon) - coindict['price_init'])
    elif coindict['name'] == 'BlackMoon':
      coindict['profit_value'] = int((coindict['satoshi']*0.00000001 * coindict['amount'] * pETHWon) - coindict['price_init'])
    elif coindict['name'] == 'Tezos' or coindict['name'] == 'Air':
      coindict['profit_value'] = int((coindict['satoshi']*0.00000001 * coindict['amount'] * pBTCWon) - coindict['price_init'])
    elif coindict['coin_price']:
      coindict['profit_value'] = int((coindict['coin_price'] * coindict['amount'] * pBTCWon) - coindict['price_init'])
    else:
      coindict['profit_value'] = 0


  total_profit_value = sum([i['profit_value'] for i in result])
  total_price_init = sum([i['price_init'] for i in result])
  refreshSec = request.args.get('refresh')
  
  return render_template('coin.html', result = result, pUSD = pUSD, pBTC = pBTC, pBTCWon = pBTCWon, pETH = pETH, pETHWon = pETHWon, pXRP = pXRP, pXRPWon = pXRPWon, total_profit_value = total_profit_value, total_price_init = total_price_init, refreshSec = refreshSec)




if __name__ == '__main__':
  app.debug=True
#  app.run(host='0.0.0.0')
  http_server = WSGIServer(('0.0.0.0', 5000), app)
  http_server.serve_forever()