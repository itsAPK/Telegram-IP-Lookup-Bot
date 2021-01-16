import requests
import telebot
import time
from telebot.apihelper import ApiException
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,Update
import os 
TOKEN=os.environ.get("BOT_TOKEN", None)
bot=telebot.TeleBot(TOKEN)

server=Flask(__name__)

def start_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 2
    a=KeyboardButton('🔎 IP Lookup')
    b=KeyboardButton('🔎 Search Subdomains')
    markup.row(a)
    markup.row(b)
    return markup

@bot.message_handler(commands=['start'])
def start_message(msg):
    bot.send_chat_action(msg.chat.id, 'typing')
    bot.send_message(msg.chat.id,'Hello ' + msg.from_user.first_name+"\nUsage 1. 🔎 *IP Lookup* to Find IP deatials\n      2. 🔎 *Search Subdomains* to search subdomains of URL",reply_markup=start_markup(),parse_mode='markdown')

@bot.message_handler(regexp='🔎 IP Lookup')
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
        bot.send_message(message.chat.id,all_data,parse_mode='markdown')
    except KeyError:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id,'❌ invalid IP address')

@bot.message_handler(regexp='🔎 Search Subdomains')
def subdomains_handler(message):
        bot.send_chat_action(message.chat.id, 'typing')
        sent = bot.send_message(message.chat.id, "Send Domain name")
        bot.register_next_step_handler(sent, domain)

def domain(message):
    file=open('subdomains-1000.txt','r')
    content=file.read()
    subdomains=content.splitlines()
    total=[]
    urls=""
    bot.send_message(message.chat.id,"*Searching subdomains,It may take minutes*",parse_mode='markdown')
    for subdomain in subdomains:
        url="http://{}.{}".format(subdomain,message.text)
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            total.append(url)
            urls+=url+"\n"
    data="✅ Domain : {}\n➖Total Subdomains : {}\n\n⚠️ Discovered subdomains:\n{}".format(message.text,len(total),urls)   
    bot.send_message(message.chat.id,data)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('APP_NAME')+".herokuapp.com/"+TOKEN)
    return "!", 200


if __name__ == "__main__":
    bot.infinity_polling(True)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
