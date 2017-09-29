import sys
import time
import telepot
from db_example import show_price_init, update_price_init, update_id

def handle(msg):
  content_type, chat_type, chat_id = telepot.glance(msg)
  print(content_type, chat_type, chat_id, msg['text'], msg['text'].split(' '))

  if content_type == 'text':
    msgList = msg['text'].split(' ')
    print(msgList)
    
    if len(msgList) == 3:
      update_price_init(msgList[0], msgList[1], (show_price_init(msgList[0])[0] - int(msgList[2])), (show_price_init(msgList[1])[0] + int(msgList[2])))
      bot.sendMessage(chat_id, 'Balance Updated.')
    elif len(msgList) == 2:
      update_id(msgList[0], msgList[1])
      bot.sendMessage(chat_id, 'ID Updated.')
    

TOKEN = '430352665:AAEd-DKnf_XezTtSWzJK-sZSBfiR1AuCdc0'

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
  time.sleep(10)