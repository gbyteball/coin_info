import requests

#def getBitcoinPrice():
#  URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
##  params = {'param1': 'value1', 'param2': 'value'}
##  response = requests.get(URL, params=params)
#  headers = {'Connection': 'keep-alive'}
#  try:
#    response = requests.get(URL, headers=headers, timeout=1)
#  except:
#    return 0;
##  response.status_code
##  response.text
#  response = response.json()
#  response = response[0]["price_usd"]
#  return float(response)

def getBittrexPrice(coin1, coin2, type):
  URL = 'https://bittrex.com/api/v1.1/public/getticker'
  params = {'market': coin1 + '-' + coin2}
  headers = {'Connection': 'keep-alive'}
  try:
    response = requests.get(URL, headers=headers, params=params, timeout=2)
  except:
    return 0;
#  response.status_code
#  response.text
  response = response.json()
  if response.get('success') == True:
    return float(response.get('result').get(type))
  else:
    return null

#def getCoinonePrice(coin):
#  URL = 'http://api.coinone.co.kr/ticker'
#  params = {'currency': coin, 'format': 'json'}
#  headers = {'Connection': 'keep-alive'}
#  try:
#    response = requests.get(URL, headers=headers, params=params, timeout=2)
#    response = response.json()
#    if response['result'] == 'success':
#      return int(response['last'])
#    else:
#      return 0
#  except:
#    return 0;

def getUSDKRW():
  URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%3D%22USDKRW%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
  headers = {'Connection': 'keep-alive'}
  try:
    response = requests.get(URL, headers=headers, timeout=1)
  except:
    return 0;
  response = response.json()
#  print response
  return float(response.get('query').get('results').get('rate').get('Rate'))




def getBittrexPrice2(coin1, coin2, type, q):
  URL = 'https://bittrex.com/api/v1.1/public/getticker'
  params = {'market': coin1 + '-' + coin2}
  headers = {'Connection': 'keep-alive'}
  try:
    response = requests.get(URL, headers=headers, params=params, timeout=2)
  except:
    q.put([coin2, 0])
    return 0;
#  response.status_code
#  response.text
  response = response.json()
  if response.get('success') == True:
    if(response.get('result').get(type) is None):
      q.put([coin2, float(0)])
    else:
      q.put([coin2, float(response.get('result').get(type))])
    return
#    return float(response['result'][type])
  else:
    q.put([coin2, 0])
    return
#    return null


def getBitfinexPrice(coin1, coin2, type, q):
  URL = 'https://api.bitfinex.com/v2/ticker/t' + coin2 + coin1
  headers = {'Connection': 'keep-alive'}
  try:
    response = requests.get(URL, headers=headers, timeout=10)
    response = response.json()
  except:
    q.put([coin2, float(0)])
    return 0;
#  response.status_code
#  response.text
  
  if(response[0] == 'error'):
    q.put([coin2, float(0)])
#    print(coin1 + '/' + coin2)
#    print(response)
  else:
#  print(response)
    q.put([coin2, float(response[6])])
  return

def getBitfinexPrices(coinlist, type, q):
  URL = 'https://api.bitfinex.com/v2/tickers?symbols=' + ','.join(coinlist)
  headers = {'Connection': 'keep-alive'}
  try:
    response = requests.get(URL, headers=headers, timeout=10)
    response = response.json()
  except:
    q.put([coin2, float(0)])
    return 0;
#  response.status_code
#  response.text
  
#  print(response)
  if(response[0] == 'error'):
#    q.put([coin2, float(0)])
#    print(coin1 + '/' + coin2)
    print(response)
  else:
    for item in response:
#      print(item[0][1:4])
#      print(float(item[7]))
#      print(' ')
      q.put([item[0][1:4], float(item[7])])

  return

def getHitbtcPrice(coin1, coin2, type, q):
  URL = 'https://api.hitbtc.com/api/2/public/ticker/' + coin2 + coin1
  headers = {'Connection': 'keep-alive'}
  try:
    response = requests.get(URL, headers=headers, timeout=10)
    response = response.json()
  except:
    q.put([coin2, float(0)])
    return 0;
#  response.status_code
#  response.text
  
  if(response.get(type) is None):
    q.put([coin2, float(0)])
#    print(coin1 + '/' + coin2)
#    print(response)
  else:
#    print(response)
    q.put([coin2, float(response.get(type))])
  return

def getUSDKRW2(a, q):
  URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%3D%22USDKRW%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
  headers = {'Connection': 'keep-alive'}
  try:
    response = requests.get(URL, headers=headers, timeout=1)
  except:
    q.put(['USDT', 0])
    return 0;
  response = response.json()
#  print response
  q.put(['USDT', float(response.get('query').get('results').get('rate').get('Rate'))])
  return
#  return float(response['query']['results']['rate']['Rate'])
