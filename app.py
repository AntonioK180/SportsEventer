from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL


app = Flask(__name__)
mysql = MySQL(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3308
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    return render_template('home.html')
