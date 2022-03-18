# sqlite_app.py
# process medium.com articles using sqlite3
import csv
import sqlite3
from sqlite3 import Error
import pandas

import config


DB = config.sqlitedb
ARTICLES_CSV = config.articles_csv
TAGS_CSV = config.articles_csv
TB1  = config.tb1


def csv_to_sql():

    con = sqlite3.connect(DB)
    cur = con.cursor()
    df = pandas.read_csv(ARTICLES_CSV)
    tb1 = TB1
    cols = f"id, title, url"
    #df.to_sql(TB1, con, if_exists='append', index=False)
    df.to_sql(TB1, con, if_exists='replace', index=False)

    filter = f"title like '%pandas%'"
    sql = f"SELECT {cols} FROM {tb1} where {filter} ;"

    rows = cur.execute(sql)
    for row in rows:
        print(row[0], row[2])

    cols = f"count(*)"
    sql = f"SELECT {cols} FROM {tb1} where {filter} ;"
    rows = cur.execute(sql).fetchall()
    count = rows[0][0]
    print("row_count:", count)

    con.commit()
    con.close()

def create_database(db):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_tables():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS article;")
    cur.execute("CREATE TABLE article(ix, id, title, url);")
    cur.execute("DROP TABLE IF EXISTS tag;")
    cur.execute("CREATE TABLE tag(tag);")
    cur.execute("DROP TABLE IF EXISTS idtag;")
    cur.execute("CREATE TABLE idtag(id, tag);")

    con.commit()
    con.close()

def load_url_table():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    a_file = open(ARTICLES_CSV)
    rows = csv.reader(a_file)
    cur.executemany("INSERT INTO articles VALUES (?, ?, ?, ?)", rows)
    cur.execute("SELECT * FROM articles LIMIT 10")
    print(cur.fetchall())



def load_tag_table(con,cur):
    a_file = open(TAGS_CSV)
    rows = csv.reader(a_file)
    cur.executemany("INSERT INTO tag VALUES (?)", rows)

def load_idtag_table(con,cur):
    pass


def load_rank_table(con,cur):
    pass


if __name__ == '__main__':
    create_database(DB)
    con = sqlite3.connect(DB)
    cur = con.cursor()
    create_tables(con,cur)
    load_url_table(con,cur)
    load_tag_table(con,cur)
    load_idtag_table(con,cur)
    con.commit()
    con.close()


