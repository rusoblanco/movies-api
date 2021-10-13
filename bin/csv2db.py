#!/usr/bin/env python3

import csv
import sqlite3
#from sqlite3 import Error

CSV_FILE = "../db/films.csv"

con = sqlite3.connect("../db/films.db")
cur = con.cursor()
cur.execute("CREATE TABLE films (year, name);")

with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
    dr = csv.DictReader(csvfile)
    to_db = [(i["year"], i["name"]) for i in dr]

cur.executemany("INSERT INTO t (year, name) VALUES (?, ?);", to_db)
con.commit()
con.close()
