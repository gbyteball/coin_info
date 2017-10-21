import requests
import json
import base64
import hashlib
import time
import hmac

bitfinexURL = 'https://api.bitfinex.com/v1/balances'

def getBitfinexBalance():
    
    with open("secrets.json") as secrets_file:
      secrets = json.load(secrets_file)
      secrets_file.close()
      bitfinexKey = secrets['bitfinexKey']
      bitfinexSecret = secrets['bitfinexSecret'].encode('UTF-8')
        
    #print("BitFinex")
    payloadObject = {
            'request':'/v1/balances',
            'nonce':str(100000*int(time.time())), #convert to string
            'options':{}
    }

    payload_json = json.dumps(payloadObject)
    #print("payload_json: ", payload_json)

    payload = base64.b64encode(bytes(payload_json))
    #print("payload: ", payload)

    m = hmac.new(bitfinexSecret, payload, hashlib.sha384)
    m = m.hexdigest()

    #headers
    headers = {
          'X-BFX-APIKEY' : bitfinexKey,
          'X-BFX-PAYLOAD' : base64.b64encode(bytes(payload_json)),
          'X-BFX-SIGNATURE' : m
    }

    r = requests.get(bitfinexURL, data={}, headers=headers)
    #print('Response Code: ' + str(r.status_code))
    #print('Response Header: ' + str(r.headers))
    #print('Response Content: '+ str(r.content))
    return str(r.content)
    
#getBitfinexBalance()