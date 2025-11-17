import sqlite3
import time
import datetime



def user_exists(user_id: int) -> bool:
    conn = sqlite3.connect("../data/Food.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE id = ?", (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return not exists



def create_table_users():
    con = sqlite3.connect("../data/Food.db")
    con.execute("""CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY,
                        lang STRING)
            """)
    con.close()




def add_new_user(id: str, lang: str):
    conn = sqlite3.connect("../data/Food.db")
    cursor = conn.cursor()
    cursor.execute("""
                            INSERT INTO Users (id, lang)
                            VALUES (?, ?)
    """, (id,lang))
    conn.commit()
    conn.close()







def create_table_log_food():
    con = sqlite3.connect("../data/Food.db")
    con.execute("""
                    CREATE TABLE IF NOT EXISTS Log_food(
                        id STRING,
                        user_id INTEGER,
                        date REAL,
                        name STRING,
                        energy REAL,
                        fat REAL,
                        carbohydrate REAL,
                        protein REAL,   
                        mass REAL
                    )"""
                )
    con.close()





def get_day_log_food(user_id, date):
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    start_timestamp = time.mktime(start_of_day.timetuple())
    current_timestamp = time.time()
    conn = sqlite3.connect("../data/Food.db")
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







def log_food(food, mass, user_id):
    conn = sqlite3.connect("../data/Food.db")
    cursor = conn.cursor()
    cursor.execute("""
                        INSERT INTO log_food (id, user_id, date, name, energy, fat, carbohydrate, protein, mass)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (food[0], user_id, int(time.time()), food[1], food[2], food[3], food[4], food[5], mass))

    conn.commit()
    conn.close()



def create_table_food():
    con = sqlite3.connect("../data/Food.db")
    con.execute("""CREATE TABLE IF NOT EXISTS Food (
                        id STRING,
                        name STRING,
                        energy REAL,
                        fat REAL, 
                        carbohydrate REAL, 
                        protein REAL)
            """)

    con.close()


def get_food(id):
    conn = sqlite3.connect("../data/Food.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Food WHERE id = ?", (str(id),))
    exists = cursor.fetchone()

    conn.close()
    return list(exists)


def search_food(name):
    conn = sqlite3.connect("../data/Food.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Food WHERE name LIKE ? LIMIT 300",(f'%{name}%',))

    res = cursor.fetchall()
    return res


def food_exists(title: str) -> bool:
    conn = sqlite3.connect("../data/Food.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Food WHERE name = ?", (title,))
    exists = cursor.fetchone() is not None

    conn.close()
    return not exists




def add_food(foods):
    conn = sqlite3.connect("../data/Food.db")
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




def create_table_search_log():
    con = sqlite3.connect("../data/Food.db")
    con.execute("""CREATE TABLE IF NOT EXISTS Search_log (
                            user_id STRING,
                            date RALE,
                            mess STRING)
                """)

    con.close()


def search_log_exists(mess: str) -> bool:
    conn = sqlite3.connect("../data/Food.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Search_log WHERE mess = ?", (mess,))
    exists = cursor.fetchone() is not None

    conn.close()
    return not exists



def add_search_log(user_id, mess: str):
    date = int(time.time())
    conn = sqlite3.connect("../data/Food.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Search_log (user_id, date, mess)
                   VALUES (?, ?, ?)""", (user_id, date, mess))

    conn.commit()
    conn.close()
