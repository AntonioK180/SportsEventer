from flask_mysqldb import MySQL
from app import mysql



cur = mysql.connection.cursor()

cur.execute('''
	CREATE TABLE Users(
		id INT PRIMARY KEY auto_increment,
		username VARCHAR(30)
	);
''')
