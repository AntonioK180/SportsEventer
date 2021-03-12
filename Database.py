import mysql.connector

mydb = mysql.connector.connect(
	host = "",
	user = "",
	password = "",
	database = "SportsEventer"
)

mycursor = mydb.cursor()


mycursor.execute('''
	CREATE TABLE Users(
		id int Primary Key not null auto_increment,
		email tinytext,
		username tinytext,
		password tinytext
	)
''')

