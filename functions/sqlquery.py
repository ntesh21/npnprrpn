import os
import sqlite3

conn = sqlite3.connect('/home/parajuli/Desktop/chatbot-api/chatModel/datasets/user_log.db',check_same_thread=False)

conn.row_factory = sqlite3.Row

# Make a convenience function for running SQL queries
def sql_query(query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def sql_edit_insert(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()

def sql_delete(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()

def sql_query2(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    rows = cur.fetchall()
    return rows