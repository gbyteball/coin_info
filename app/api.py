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
  if response['success'] == True:
    return float(response['result'][type])
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
  return float(response['query']['results']['rate']['Rate'])
