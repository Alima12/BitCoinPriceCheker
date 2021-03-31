import sqlite3
from datetime import datetime,timedelta

connect = sqlite3.connect("dataprices.db")
cursor = connect.cursor()
def create():
    q = """create table if not exists Prices(
        symbol VACHAR,
        buy INT,
        sell INT,
        sec DATETIME NOT NULL default CURRENT_TIMESTAMP
    );"""
    cursor.execute(q)


def insert(buy,sell):
    time = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    q = f"""INSERT INTO Prices VALUES("USD",{buy},{sell},'{time}');"""
    cursor.execute(q)
    connect.commit()


def bestWeek(buy):
    time = datetime.now() - timedelta(7)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT count(*) FROM Prices where sec > "{time}" and buy < {buy}; """
    res = cursor.execute(q)
    for item in res:
        count = item[0]
    if count == 0:
        return True
    return False

def bestMonth(buy):
    time = datetime.now() - timedelta(30)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT count(*) FROM Prices where sec > "{time}" and buy < {buy}; """
    res = cursor.execute(q)
    for item in res:
        count = item[0]
    if count == 0:
        return True
    return False

def bestThree(buy):
    time = datetime.now() - timedelta(3)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT count(*) FROM Prices where sec > "{time}" and buy < {buy}; """
    res = cursor.execute(q)
    for item in res:
        count = item[0]
    if count == 0:
        return True
    return False

def MostWeek(buy):
    time = datetime.now() - timedelta(7)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT count(*) FROM Prices where sec > "{time}" and buy > {buy}; """
    res = cursor.execute(q)
    for item in res:
        count = item[0]
    if count == 0:
        return True
    return False

def MostMonth(buy):
    time = datetime.now() - timedelta(30)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT count(*) FROM Prices where sec > "{time}" and buy > {buy}; """
    res = cursor.execute(q)
    for item in res:
        count = item[0]
    if count == 0:
        return True
    return False

def MostThree(buy):
    time = datetime.now() - timedelta(3)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT count(*) FROM Prices where sec > "{time}" and buy > {buy}; """
    res = cursor.execute(q)
    for item in res:
        count = item[0]
    if count == 0:
        return True
    return False


def min_max_today():
    time = datetime.now()
    begin = time.strftime("%y/%m/%d 00:00:00")
    end =  time.strftime("%y/%m/%d 23:59:59")
    q= f"SELECT min(buy),max(buy) FROM Prices WHERE '{begin}'  <= sec AND sec <= '{end}';"
    res = cursor.execute(q)
    for row in res:
        return row

def min_max_yesterday():
    time = datetime.now() - timedelta(1)
    begin = time.strftime("%y/%m/%d 00:00:00")
    end =  time.strftime("%y/%m/%d 23:59:59")
    q= f"SELECT min(buy),max(buy) FROM Prices WHERE '{begin}'  <= sec AND sec <= '{end}';"
    res = cursor.execute(q)
    for row in res:
        return row


def growth(day,price):
    time = datetime.now() - timedelta(day)
    begin = time.strftime("%y/%m/%d 00:00:00")
    end =  time.strftime("%y/%m/%d 23:59:59")
    print(end,begin)
    q= f"SELECT buy FROM Prices Where sec < '{end}' and sec >  '{begin}' ORDER BY sec  LIMIT 1;"
    res = cursor.execute(q)
    for row in res:
        past = row[0]
    dif = (price - past) / past * 100
    dif = round(dif,2)
    return dif

create()



