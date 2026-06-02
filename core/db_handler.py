import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "database"))
os.makedirs(DB_DIR, exist_ok=True)

DB_FILE = os.path.join(DB_DIR, "buses.db")
con = sqlite3.connect(DB_FILE, check_same_thread=False)
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS buses (
    Bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Bus_capacity INTEGER NOT NULL,
    Bus_destination TEXT NOT NULL,
    Departure_time TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS reservation (
    Res_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Bus_id INTEGER NOT NULL,
    First_name TEXT NOT NULL,
    Middle_name TEXT NOT NULL,
    Last_name TEXT NOT NULL,
    Phone_number TEXT NOT NULL,
    FOREIGN KEY (Bus_id) REFERENCES buses (Bus_id),
    UNIQUE (Bus_id, First_name, Middle_name, Last_name, Phone_number)
)
""")

con.commit()


def Get_Bus_Time(bus_id):
    cur.execute("SELECT Departure_time FROM buses WHERE Bus_id = ?", (bus_id,))
    result = cur.fetchone()
    return result[0] if result else None


def Add_Bus(capacity, destination, departure_time):
    cur.execute(
        "INSERT INTO buses (Bus_capacity, Bus_destination, Departure_time) VALUES (?, ?, ?)",
        (capacity, destination, departure_time),
    )
    con.commit()


def Del_Bus(bus_id):
    cur.execute("DELETE FROM buses WHERE Bus_id = ?", (bus_id,))
    con.commit()
    cur.execute("SELECT COUNT(*) FROM buses")
    if cur.fetchone()[0] == 0:
        cur.execute("DELETE FROM sqlite_sequence WHERE name='buses'")
        con.commit()


def Show_Buses():
    cur.execute("SELECT * FROM buses")
    return cur.fetchall()
