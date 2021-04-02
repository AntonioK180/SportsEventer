from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import mydb


cursor = mydb.cursor()


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



    def get_user_by_username(username):
        query = 'SELECT * FROM Users WHERE username = %s'
        value = (username,)
        cursor.execute(query, value)
        row = cursor.fetchone()
        print(row)
        if row is None:
            return
        else:
            return User(*row)

    def get_user_by_email(email):
        query = 'SELECT * FROM Users WHERE email = %s'
        value = (email,)
        cursor.execute(query, value)
        row = cursor.fetchone()
        if row is None or row is False:
            return
        else:
            return User(*row)

    @staticmethod
    def hash_password(pwd):
        return generate_password_hash(pwd)

    def verify_password(self, submit_password):
        return check_password_hash(self.password, submit_password)
