# -*- coding: utf-8 -*-

import sys
import time
import telepot
from db_example import show_price_init, update_price_init, update_id, update_satoshi

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def handle(msg):
  content_type, chat_type, chat_id = telepot.glance(msg)
  print(content_type, chat_type, chat_id, msg['text'], msg['text'].split(' '))

  if content_type == 'text':
    msgList = msg['text'].split(' ')
    print(msgList)
    
    if len(msgList) == 1 and msgList[0] == '/help':
      bot.sendMessage(chat_id, 'id1 id2 balance : id1에서 id2로 balance만큼 금액 이동\nid1 id2 : id1을 id2로 수정\ncode satoshi : code에 해당하는 코인의 satoshi 가격 설정 (USDT인 경우 환율 설정)')
    elif len(msgList) == 3:
      update_price_init(msgList[0], msgList[1], (show_price_init(msgList[0])[0] - int(msgList[2])), (show_price_init(msgList[1])[0] + int(msgList[2])))
      bot.sendMessage(chat_id, 'Balance Updated.')
    elif len(msgList) == 2:
      if(isNumber(msgList[0])):
        update_id(msgList[0], msgList[1])
        bot.sendMessage(chat_id, 'ID Updated.')
      else:
        update_satoshi(msgList[0], msgList[1])
        if(msgList[0] == 'usdt'):
          bot.sendMessage(chat_id, 'USD/KRW Updated.')
        else:
          bot.sendMessage(chat_id, 'Satoshi Updated.')
    

TOKEN = '430352665:AAEd-DKnf_XezTtSWzJK-sZSBfiR1AuCdc0'

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
  time.sleep(10)
