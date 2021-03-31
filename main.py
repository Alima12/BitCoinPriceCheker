import requests as req
import sqlite3
from connectToDb import insert,bestWeek,bestMonth,bestThree,MostMonth,MostWeek,MostThree,min_max_today,min_max_yesterday,growth
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime

updater = Updater(token='1716430763:AAEuqY-YqLMfYO5PKU_lkJ73bJ4PvxLjGSs', use_context=True)
bot = updater.bot

def send_notif(message):
    bot.send_message(88171378,message)
    bot.send_message(-1001341117324,message)


def get_growth(price):
    days = [0,3,7,30]
    text = "\n\n⚡️میزان رشد:\n\n"
    def change_form(dif):
        dif = str(dif)
        if '-' in dif:
            dif = dif.replace('-','')
            dif = dif + '➖ '
        else:
            dif = dif +  "➕ " 

        return dif

    for day in days:
        dif = growth(day,price)
        if day == 0:
            dif = change_form(dif)
            t= f"☀️ امروز => %{dif}\n"
        else:
            dif = change_form(dif)
            t= f"📊 از {day} روز پیش => %{dif}\n"
        text += t
    return text



def more_detail():
    min_t,max_t = min_max_today()
    min_y,max_y = min_max_yesterday()
    text = f"\n\n 🏵🎗بیشتر🎗🏵\n\n🥇کمترین قیمت امروز => {min_t}\n🥈بیشترین قیمت امروز=> {max_t}\n\n🥇بیشترین قیمت دیروز=> {min_y}\n🥈کمترین  قیمت دیروز => {max_y} \n\n\n"
    return text


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




    insert(price["buy"],price["sell"])



    if len(message) > 1:
        more = more_detail()
        message.append(more)
        gro = get_growth(buy_price)
        message.append(gro)
        __time = datetime.now().strftime("%H:%M:%S")
        message.append(__time)
        msg = '\n'.join(message)
        send_notif(msg)



if __name__ == "__main__":
    set_price()
