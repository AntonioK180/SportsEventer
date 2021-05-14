from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import mydb


cursor = mydb.cursor(buffered=True)


class User:
    def __init__(self, user_id, email, username, password):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.password = password

    def create(self):
        query = 'INSERT INTO Users (email, username, pwd) VALUES (%s, %s, %s)'
        value = (self.email, self.username, self.password)
        cursor.execute(query, value)
        mydb.commit()
        return 1


    @staticmethod
    def get_user_by_username(username):
        query = 'SELECT * FROM Users WHERE username = %s'
        value = (username,)
        cursor.execute(query, value)
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return User(*row)

    @staticmethod
    def get_user_by_id(user_id):
        query = 'SELECT * FROM Users WHERE user_id = %s'
        value = (user_id,)
        cursor.execute(query, value)
        row = cursor.fetchone()
        if row is None:
            return
        else:
            return User(*row)

    @staticmethod
    def get_joined_events(user_id):
        query = 'SELECT event_id FROM UsersEvents WHERE user_id=%s'
        value = (user_id,)
        cursor.execute(query, value)
        result = cursor.fetchall()
        events = []
        if result is None:
            return;
        else:
            for row in results:
                events.append(Event.find(*row))
            if len(events) == 0:
                return;
            else:
                return events


    @staticmethod
    def hash_password(pwd):
        return generate_password_hash(pwd)

    def verify_password(self, submit_password):
        return check_password_hash(self.password, submit_password)
