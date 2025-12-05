import sqlite3
import time
import datetime
from app.core.config import DB_PATH
from urllib.parse import unquote
from app.api.schemas import LogFood, SearchLog


def user_exists(user_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE id = ?", (user_id,))
    exists = cursor.fetchone() is None
    conn.close()
    return not exists




def add_new_user(id: str, lang: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                            INSERT INTO Users (id, lang)
                            VALUES (?, ?)
    """, (id,lang))
    conn.commit()
    conn.close()




def get_day_log_food(user_id, date):
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    start_timestamp = time.mktime(start_of_day.timetuple())
    current_timestamp = time.time()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if "-" not in date:
        cursor.execute("""
                            SELECT * FROM Log_food 
                            WHERE user_id = ? 
                            AND date BETWEEN ? AND ? 
                            ORDER BY date
        """,(user_id,start_timestamp,current_timestamp))

    res = [list(i) for i in cursor.fetchall()]
    conn.close()
    return res



def log_food(food: LogFood):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print(food)
    cursor.execute("""
                        INSERT INTO log_food (id, user_id, date, name, energy, fat, carbohydrate, protein, mass)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        food.id,
        food.user_id,
        food.date,
        food.name,
        food.energy,
        food.fat,
        food.carbohydrate,
        food.protein,
        food.mass))

    conn.commit()
    conn.close()


def get_food(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Food WHERE id = ?", (str(id),))
    exists = cursor.fetchone()

    conn.close()
    try:
        true = exists[0]
        return list(exists)
    except:
        return None

def search_food(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Food WHERE name LIKE ? LIMIT 300",(f'%{name}%',))
    res = cursor.fetchall()
    return list(res)



def food_exists(title: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Food WHERE name = ?", (title,))
    exists = cursor.fetchone() is not None

    conn.close()
    return not exists



def add_food(foods):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for i in foods:
        if food_exists(i["title"]):
            try:
                cursor.execute("""
                                    INSERT INTO Food (id, name, energy, fat, carbohydrate, protein)
                                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (i["id"], i["title"], float(i["energy"].replace(",",".")), float(i["fat"].replace(",",".")), float(i["carbohydrate"].replace(",",".")), float(i["protein"].replace(",","."))))
                conn.commit()
            except:
                continue

    conn.close()



def search_log_exists(mess: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Search_log WHERE mess = ?", (mess,))
    exists = cursor.fetchone() is not None

    conn.close()
    return not exists



def add_search_log(search_log:SearchLog):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Search_log (user_id, date, mess)
                   VALUES (?, ?, ?)""", (search_log.user_id, search_log.date, search_log.mess))

    conn.commit()
    conn.close()
