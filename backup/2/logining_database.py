import sqlite3
import uuid
from datetime import datetime
import hashlib


class Database:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT,
                birth_date TEXT,
                department TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def create_user(self, email, password, first_name="", last_name="", middle_name=""):
        # Генерируем UID в формате 77021{номер}
        self.cursor.execute('SELECT COUNT(*) FROM users')
        count = self.cursor.fetchone()[0]
        uid = f"77021{count + 1:05d}"

        # Хешируем пароль
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            self.cursor.execute('''
                INSERT INTO users (uid, email, password_hash, first_name, last_name, middle_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (uid, email, password_hash, first_name, last_name, middle_name))
            self.conn.commit()
            return uid
        except sqlite3.IntegrityError:
            return None

    def authenticate_user(self, email, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        self.cursor.execute('''
            SELECT * FROM users WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))

        user = self.cursor.fetchone()
        if user:
            columns = [description[0] for description in self.cursor.description]
            return dict(zip(columns, user))
        return None

    def update_user_profile(self, uid, first_name, last_name, middle_name, birth_date, department):
        self.cursor.execute('''
            UPDATE users 
            SET first_name = ?, last_name = ?, middle_name = ?, 
                birth_date = ?, department = ?
            WHERE uid = ?
        ''', (first_name, last_name, middle_name, birth_date, department, uid))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_user_by_uid(self, uid):
        self.cursor.execute('SELECT * FROM users WHERE uid = ?', (uid,))
        user = self.cursor.fetchone()
        if user:
            columns = [description[0] for description in self.cursor.description]
            return dict(zip(columns, user))
        return None

    def get_user_by_email(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = self.cursor.fetchone()
        if user:
            columns = [description[0] for description in self.cursor.description]
            return dict(zip(columns, user))
        return None

    def close(self):
        self.conn.close()