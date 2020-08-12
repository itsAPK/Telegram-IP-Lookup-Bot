import requests
import telebot
import time
import phonenumbers
from phonenumbers import carrier
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton
token="s"
bot=telebot.TeleBot(token)

'''server=Flask(__name__)'''

def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    a=InlineKeyboardButton(' 🔎 IP Lookup',callback_data='short')
    c=InlineKeyboardButton('ℹ️ Help',callback_data='help')
    markup.add(a)
    
    markup.add(c)
    return markup

@bot.message_handler(commands=['start'])
def start_message(msg):
    bot.send_chat_action(msg.chat.id, 'typing')
    bot.send_message(msg.chat.id,'Hello ' + msg.from_user.first_name,reply_markup=start_markup())

@bot.message_handler(commands=['iplookup'])
def ip_handler(message):    
    bot.send_chat_action(message.chat.id, 'typing')
    sent = bot.send_message(message.chat.id, "Send IP address")
    bot.register_next_step_handler(sent, ip)


def ip(message):
    ip=message.text
    url='http://ip-api.com/json/{}?fields=country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp'.format(ip)
    r=requests.get(url).json()
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,'fetching...')
    try: 
        country=r['country']
        countryCode=r['countryCode']
        region=r['region']
        regionName=r['regionName']
        city=r['city']
        zip_=r['zip']
        lat=r['lat']
        lon=r['lon']
        isp=r['isp']
        timezone=r['timezone']
        all_data=f'🚩*Details of* {message.text}\n\n🌐 *country :* {country}\n➖ *countryCode :* {countryCode}\n🏷 *region :* {region}\n🔺 *regionName :* {regionName} \n✅ *city :* {city}\n📍 *zipCode :* {zip_}\n📌 *latitude :* {lat}\n📌 *longitude :* {lon}\n⏰ *timezone :* {timezone}\n⚙️ *isp :* {isp}'
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id,all_data)
    except KeyError:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id,'❌ invalid IP address')



while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		time.sleep(1)
