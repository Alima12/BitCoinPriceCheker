import requests as req
import sqlite3
from connectToDb import insert,bestWeek,bestMonth,bestThree,MostMonth,MostWeek,MostThree
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime

updater = Updater(token='1716430763:AAEuqY-YqLMfYO5PKU_lkJ73bJ4PvxLjGSs', use_context=True)
bot = updater.bot

def send_notif(message):
    bot.send_message(88171378,message)
    bot.send_message(-1001341117324,message)

def set_price():
    url = "https://blockchain.info/ticker"
    response = req.get(url)
    response = response.json()
    price = response["USD"]
    buy_price = price["buy"]
    message = []
    title = f"📌قیمت کنونی بیتکوین=>   {buy_price} دلار \n"
    message.append(title)
    if bestThree(buy_price):
        message.append(f"🔔 کمترین قیمت در 3 روز گذشته")
    if bestWeek(buy_price):
        message.append(f"🔔 کمترین قیمت در  7 روز گذشته")
    if bestMonth(buy_price):
        message.append(f"🔔 کمترین قیمت در  30 روز گذشته")
    if MostThree(buy_price):
        message.append(f"🔔 بیشترین قیمت در 3 روز گذشته")
    if MostWeek(buy_price):
        message.append(f"🔔 بیشترین قیمت در  7 روز گذشته")
    if MostMonth(buy_price):
        message.append(f"🔔 بیشترین قیمت در  30 روز گذشته")

    if len(message) > 1:
        __time = datetime.now().strftime("%H:%M:%S")
        message.append(__time)
        msg = '\n'.join(message)
        send_notif(msg)
    insert(price["buy"],price["sell"])



if __name__ == "__main__":
    set_price()
