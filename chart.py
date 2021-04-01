from ImageCharts import ImageCharts
import random


def draw_chart(data):
    items = [str(i) for i in data]
    random.shuffle(items)
    items_str = ",".join(items)
    pie = ImageCharts().chco("3498db").chdl("BuyPrice").chdlp('b').chma("50,20,60,30").chs("999x300").cht('ls:nda').chts("f1c40f,25").chtt("BitCoin BuyPrice Chart")\
        .chd("t:{}".format(items_str))

    with open("chart.jpg",'wb') as file:
        file.write(pie.to_binary())

    return 'chart.jpg'