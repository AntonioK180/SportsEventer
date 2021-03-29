from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from app import db

app = Flask(__name__)

cursor = db.cursor()

class User:
	def __init__(self, user_id, email, username, password):
		self.user_id = user_id
		self.email = email
		self.username = username
		self.password = password

	def create(self):
		cursor.execute('INSERT INTO Users (email, username, pwd) VALUES (%s, %s, %s)', (self.email, self.username, self.password))
		db.commit()
		return 1

	def get_user_by_username(username):
		cursor.execute('SELECT * FROM Users WHERE username = "%s"', (username))
		row = cursor.fetchall()
		if row is None or False:
			return None
		else:
			return User(*row)

	def get_user_by_email(email):
		cursor.execute('SELECT * FROM Users WHERE email = "%s"', (email))
		row = cursor.fetchall()
		if row is None or False:
			return None
		else:
			return User(*row)


	@staticmethod	
	def hash_password(pwd):
		return generate_password_hash(pwd)

	def verify_password(self, submit_password):
		return check_password_hash(self.password, submit_password)
