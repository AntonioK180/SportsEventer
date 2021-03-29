from flask import Flask, redirect, render_template, request, url_for
import mysql.connector

db = mysql.connector.connect(
	host="",
	user="",
	password="",
	database="SportsEventer"
)


from user import User

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	elif request.method == 'POST':
		values = (
			None,
			request.form['email'],
			request.form['username'],
			User.hash_password(request.form['pwd'])
		)
		User(*values).create()
		return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		user = request.form['user']
		pwd = request.form['pwd']
		username = User.get_user_by_username(user)
		email = User.get_user_by_email(user)
		if username is not None:
			if username.verify_password(pwd) is True:
				return redirect('/events')
			else:
				return redirect('/login')
		elif email is not None:
			if email.verify_passwoord(pwd) is True:
				return redirect('/events')
			else:
				return redirect('/login')
		else:
			return redirect('/login')
		
@app.route('/events')
def show_events():
	return render_template('events.html')

if __name__ == '__main__':
	app.run()
