import requests as req
import sqlite3
from connectToDb import insert,min_max_today,min_max_yesterday,growth,Most,Least,data
from telegram.ext import Updater
from datetime import datetime
from chart import draw_chart


#وصل شدن به ربات
updater = Updater(token='1716430763:AAEuqY-YqLMfYO5PKU_lkJ73bJ4PvxLjGSs', use_context=True)

#گرفتن ربات برای استفاده مستقیم از دستورات
bot = updater.bot


#این متود برای ارسال اعلان استفاده میشه
def send_notif(message):
    # گرفتن دیتا برای کشیدن نمودار ۶ ساعت اخیر
    datas = data()

    #عملیات کشیدن نمودار و ذخیره عکس
    # عکس رو با اسم chart.jpg توی روت زخیره میکنه
    draw_chart(datas)
    message = "🌪تغییرات قیمت در 6 ساعت اخیر🔥 \n\n" + message

    #باز کردن عکس نمودار برای ارسال 
    #ارسال عکس به کاربران انتخابی
    with open('chart.jpg','rb') as file:
        bot.send_photo(88171378,photo=file,caption=message)
        bot.send_photo(-1001341117324,photo=file,caption=message)
        bot.send_photo(1074680699,photo=file,caption=message)


#این متود درصد رشد بیت کوین رو محاسبه میکند در بازه های زمانی مختلف
#قیمت کنونی را دریافت میکند

"""
این متود اولین قیمت بازه
 مورد نظر را در همان روز - بطور مثال:
 اولین قیمتی که ۳۰ روز پیش ثبت شده باشد
 را میگیره و با قیمت کنونی مقایسه میکند
 و درصد رشد را محسابه میکند
"""
def get_growth(price):
    days = [0,3,7,30]
    text = "\n\n⚡️میزان رشد:\n\n"

    #فقط متن ارسالی را زیبا میکنه
    def change_form(dif):
        dif = str(dif)
        if '-' in dif:
            dif = dif.replace('-','')
            dif = dif + '➖ '
        else:
            dif = dif +  "➕ " 

        return dif
    
    #سه بازه زمانی 3,7 و 30 رو بررسی میکنه و درصد رشدشون رو محسابه میکنه
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


#  بیشترین و کمترین قیمت امروز و دیروز را برمیگرداند
def more_detail():
    #بیشترین و کمترین قیمت امروز
    min_t,max_t = min_max_today()
    #بیشترین و کمترین قیمت دیروز
    min_y,max_y = min_max_yesterday()
    text = f"\n\n 🏵🎗بیشتر🎗🏵\n\n🥇کمترین قیمت امروز => {min_t}\n🥈بیشترین قیمت امروز=> {max_t}\n\n🥇بیشترین قیمت دیروز=> {min_y}\n🥈کمترین  قیمت دیروز => {max_y} \n\n\n"
    return text

#هسته اصلی این برنامه
#قیمت را گرفته و به پایگاه داده میدهد
#قیمت را چک میکند و در صورت برقرار بودن شرط اعلان را صدا میزند
def set_price():
    url = "https://blockchain.info/ticker"
    response = req.get(url)
    response = response.json()
    #جدا کردن قیمت دلاری
    price = response["USD"]
    #گرفتن قیمت خرید بیت کوین
    buy_price = price["buy"]
    # لیست پیام ها که در صورتی که رویدادی رخ نداده باشد تعداد اعضای آن یک میباشید
    message = []
    #عنوان پیام ارسالی برای ارسال اعلان
    title = f"📌قیمت کنونی بیتکوین=>   {buy_price} دلار \n"
    message.append(title)
    """
    سه بازه زمانی 3 و 7 و 30 روز را چک میکند
    اگر قیمت کنونی که در بالا گرفته شد
    کمترین یا بیشترین قیمت در آن بازه زمانی باشد
    یک رویداد را به اعلان ها اضافه میکند
    """
    for day in [3,7,30]:
        #اگر قیمت کنونی بیشترین قیمت در بازه زمانی باشد
        if Most(buy_price,day):
            message.append(f"🔔 بیشترین قیمت در  {day} روز گذشته")
        #اگر قیمت کمترین قیمت در بازه زمانی باشد
        if Least(buy_price,day):
            message.append(f"🔔 کمترین قیمت در {day} روز گذشته")

    #بعد از چک کردن قیمت و ست کردن اعلان ها قیمت کنونی را نیز به پایگاه داده اضافه میکند 
    insert(price["buy"],price["sell"])


    #چک میشود اگر تعداد اعضای لیست پیام بیشتر از  1 باشد
    #که به این معنی هست رویدادی رخ داده است
    #در این صورت اعلان را آماده و ارسال میکند
    if len(message) > 1:
        #گرفتن جزيیات بیشتر مثل کمترین و  بیشترین قیمت در دیروز و امروز
        more = more_detail()
        message.append(more)
        #محسابه درصد رشد
        gro = get_growth(buy_price)
        message.append(gro)
        #گرفتن زمان و اضافه کردن آن به انتهای لیست پیام 
        __time = datetime.now().strftime("%H:%M:%S")
        message.append(__time)
        #لیست را به صورت رشته در میاریم تا قابل ارسال به عنوان اعلان باشد
        msg = '\n'.join(message)
        #دادن متن آماده به متود ارسال اعلان
        send_notif(msg)



if __name__ == "__main__":
    set_price()
