from flask import Flask, render_template, request
import sqlalchemy
from db_example import show_tables
from api import getBitcoinPrice, getBittrexPrice, getCoinonePrice, getUSDKRW
from gevent.wsgi import WSGIServer

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
  total_price_init = sum([i['price_init'] for i in result])

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

  pPAY = getBittrexPrice('BTC', 'PAY', 'Last')
  pGBYTE = getBittrexPrice('BTC', 'GBYTE', 'Last')
  pEDG = getBittrexPrice('BTC', 'EDG', 'Last')
  pSNT = getBittrexPrice('BTC', 'SNT', 'Last')
  pADX = getBittrexPrice('BTC', 'ADX', 'Last')
  pOMG = getBittrexPrice('BTC', 'OMG', 'Last')
  pDASH = getBittrexPrice('BTC', 'DASH', 'Last')
  pZEC = getBittrexPrice('BTC', 'ZEC', 'Last')
  pGNT = getBittrexPrice('BTC', 'GNT', 'Last')
  pNXT = getBittrexPrice('BTC', 'NXT', 'Last')
  pSTRAT = getBittrexPrice('BTC', 'STRAT', 'Last')
  pQTUM = getBittrexPrice('BTC', 'QTUM', 'Last')
  pKMD = getBittrexPrice('BTC', 'KMD', 'Last')
  pNMR = getBittrexPrice('BTC', 'NMR', 'Last')

  refreshSec = request.args.get('refresh')
  
  return render_template('coin.html', result = result, pUSD = pUSD, pBTC = pBTC, pBTCWon = pBTCWon, pETH = pETH, pETHWon = pETHWon, pPAY = pPAY, pGBYTE = pGBYTE, pEDG = pEDG, pSNT = pSNT, pADX = pADX, pOMG = pOMG, pDASH = pDASH, pZEC = pZEC, pGNT = pGNT, pNXT = pNXT, pSTRAT = pSTRAT, pQTUM = pQTUM, pKMD = pKMD, pNMR = pNMR, pXRP = pXRP, pXRPWon = pXRPWon, total_price_init = total_price_init, refreshSec = refreshSec)

if __name__ == '__main__':
  app.debug=True
#  app.run(host='0.0.0.0')
  http_server = WSGIServer(('0.0.0.0', 5000), app)
  http_server.serve_forever()