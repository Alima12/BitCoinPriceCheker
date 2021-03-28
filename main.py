import requests as req
import sqlite3
from connectToDb import insert,bestWeek,bestMonth,bestThree,MostMonth,MostWeek,MostThree
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


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
    if bestThree(buy_price):
        send_notif(f"کمترین قیمت در 3 روز گذشته : {buy_price}")
    if bestWeek(buy_price):
        send_notif(f"کمترین قیمت در  7 روز گذشته : {buy_price}")
    if bestMonth(buy_price):
        send_notif(f"کمترین قیمت در  30 روز گذشته : {buy_price}")

    if MostThree(buy_price):
        send_notif(f"بیشترین قیمت در 3 روز گذشته : {buy_price}")
    if MostWeek(buy_price):
        send_notif(f"بیشترین قیمت در  7 روز گذشته : {buy_price}")
    if MostMonth(buy_price):
        send_notif(f"بیشترین قیمت در  30 روز گذشته : {buy_price}")

    insert(price["buy"],price["sell"])



if __name__ == "__main__":
    set_price()
