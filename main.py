import requests as req
import sqlite3
from connectToDb import insert,min_max_today,min_max_yesterday,growth,Most,Least,data
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime
from chart import draw_chart

updater = Updater(token='1716430763:AAEuqY-YqLMfYO5PKU_lkJ73bJ4PvxLjGSs', use_context=True)
bot = updater.bot

def send_notif(message):
    datas = data()
    draw_chart(datas)
    message = "تغییرات قیمت در 6 ساعت اخیر \n\n" + message
    with open('chart.jpg','rb') as file:
        bot.send_photo(88171378,photo=file,caption=message)
        bot.send_photo(-1001341117324,photo=file,caption=message)
        bot.send_photo(1074680699,photo=file,caption=message)


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

    for day in [3,7,30]:
        if Most(buy_price,day):
            message.append(f"🔔 بیشترین قیمت در  {day} روز گذشته")
        if Least(buy_price,day):
            message.append(f"🔔 کمترین قیمت در {day} روز گذشته")


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
