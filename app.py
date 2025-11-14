from flask import Flask, render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

DB_path = f"D:\\Flask CRUD\example.db"

#Database setup
def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

#Get all users from the database
def get_users():
    conn=sqlite3.connect(DB_path)
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

#Add a users to the database
def add_user(name, age):
    conn=sqlite3.connect(DB_path)
    cursor=conn.cursor()
    cursoe.execute('INSERT into users (name, age) VALUES (?, ?)',(name, age) )
    conn.commit()
    conn.close()