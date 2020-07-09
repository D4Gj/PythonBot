import requests
import os
from bs4 import BeautifulSoup
from telebot import TeleBot, apihelper, types
from time import sleep
import  config
from datetime import datetime, date, time
import asyncio
import threading
import sys

tb = TeleBot(config.Token)
ip = '158.58.182.101'
port = '1080'

number=2
#добавить gitguardian
#не работает смена прокси :C /// Для смены прокси поменять цифру number от 1 до 10
proxy = {
    'http': 'http://lcdydnxn-'+str(number)+':3ekg17pfkoft@p.webshare.io:80',
    'https': 'https://lcdydnxn-'+str(number)+':3ekg17pfkoft@p.webshare.io:80'
}
# proxy = {
#     'http': 'http://lcdydnxn-'+str(number)+':3ekg17pfkoft@p.webshare.io:80',
#     'https': 'https://lcdydnxn-'+str(number)+':3ekg17pfkoft@p.webshare.io:80'
# }

exclude_words = ['Сувенирный','Капсула с автографом']
chat_id = 123
sleep_time = 5 #больше 5 ибо бан на айпи прилетает, тк возможно 12 запросов в минуту сделать только
stoper = True

def __init__(self, number):
        self.number = number

def getNum(self):
	return self.number

@tb.message_handler(commands=["start"])
def message(message):
 tb.send_message(message.chat.id,"Starting...")
 threading.Thread(target=start(chat_id=message.chat.id)).start()

@tb.message_handler(commands=["stop"])
def message(message):
 tb.send_message(message.chat.id,str(threading.current_thread().is_alive()))
 tb.send_message(message.chat.id,"Моя остановочка")
 sys.exit()


def get_price(hash_name):
	try:
		response = requests.get('https://steamcommunity.com/market/priceoverview/?appid=730&country=US&currency=1&market_hash_name=' + hash_name,proxies=proxy)
		return response.json()['lowest_price']
	except Exception as e:
		print('error passed', e)

def start(chat_id):
	CanWork=0
	number=1
	os.system('cls')
	while True:
		tb.send_message(chat_id, "work " +str(datetime.strftime(datetime.now(),"%H:%M:%S")))
		try:
			response = requests.get('https://steamcommunity.com/market/recent?country=RU&language=russian&currency=1',proxies=proxy)
		except Exception as e:
			print('error passed', e)
			continue
		response_json = response.json()
		if not response_json:
			sleep(sleep_time)
			tb.send_message(chat_id,"work but blocked "+str(number)+" "+str(datetime.strftime(datetime.now(),"%H:%M:%S")))
			tb.send_message(chat_id,proxy.values())
			CanWork+=1
			if CanWork==10:
				self.number+=1
				number+=1
			continue
		contexts = response_json.get('assets', {}).get('730', {})
		for context in contexts:
			for item_id, item in contexts[context].items():
				stickers = []
				if any(k in item['market_name'] for k in exclude_words):
					continue
				for description in item.get('descriptions'):
					if 'Наклейка' in description['value']:
						description_html = BeautifulSoup(description['value'], 'lxml')
						try:
							stickers_string = description_html.get_text().split('Наклейка: ')[1]
						except IndexError:
							stickers_string = description_html.get_text()
						for k in stickers_string.strip().split(','):
							stickers.append(k.strip())
				if len(stickers) > 0:
					price = get_price(item['market_hash_name'])
					for k in response_json['listinginfo'].values():
						if k['asset']['id'] == item_id:
							try:
								item_price = (k['converted_fee'] + k['converted_price']) / 100
							except KeyError:
								item_price = 'Продано!'
					stickers_text = '  -- ' + '\n  -- '.join(k.strip() for k in stickers)
					message_text = '\n'.join([item['market_name'],
											  'Минимальная цена: ' + str(price),
											  'Цена этого предмета: $' + str(item_price),
											  'Наклейки:',
											  stickers_text])
					markup = types.InlineKeyboardMarkup()
					markup.add(
						types.InlineKeyboardButton('Открыть ТП', "https://steamcommunity.com/market/listings/730/" + item['market_hash_name'])
					)
					tb.send_message(chat_id, message_text, reply_markup=markup)
		sleep(sleep_time)

def startBot():
	tb.polling(none_stop=True)

if __name__ == "__main__":
	threading.Thread(target=startBot).start()
