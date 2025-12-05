import sqlite3
import time
import datetime
from app.core.config import DB_PATH
print(DB_PATH)


def create_table_users():
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY,
                        lang STRING)
            """)
    con.close()



def create_table_log_food():
    con = sqlite3.connect(DB_PATH)
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



def create_table_food():
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS Food (
                        id STRING,
                        name STRING,
                        energy REAL,
                        fat REAL, 
                        carbohydrate REAL, 
                        protein REAL)
            """)

    con.close()



def create_table_search_log():
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS Search_log (
                            user_id STRING,
                            date RALE,
                            mess STRING)
                """)

    con.close()