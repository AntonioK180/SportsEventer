from flask import Flask, render_template
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)
mysql = MySQL(app)


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
