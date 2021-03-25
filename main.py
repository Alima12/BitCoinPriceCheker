import requests as req
import sqlite3
from connectToDb import insert,bestWeek,bestMonth
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


updater = Updater(token='1716430763:AAEuqY-YqLMfYO5PKU_lkJ73bJ4PvxLjGSs', use_context=True)
bot = updater.bot
def set_price():
    url = "https://blockchain.info/ticker"
    response = req.get(url)
    response = response.json()
    price = response["USD"]
    buy_price = price["buy"]
    if bestWeek(buy_price):
        bot.send_message(88171378,f"Best Price on 7 Days Ago: {buy_price}")
        bot.send_message(-1001341117324,f"Best Price on 7 Days Ago: {buy_price}")
    if bestMonth(buy_price):
        bot.send_message(88171378,f"Best Price on 30 Days Ago: {buy_price}")
        bot.send_message(-1001341117324,f"Best Price on 30 Days Ago: {buy_price}")

    insert(price["buy"],price["sell"])



if __name__ == "__main__":
    set_price()
