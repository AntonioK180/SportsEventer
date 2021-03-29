import yaml
import mysql.connector


db = yaml.load(open('db.yaml'))
mydb = mysql.connector.connect(
    host=db['mysql_host'],
    user=db['mysql_user'],
    password=db['mysql_password'],
    database="SportsEventer"
)

cur = mydb.cursor()

cur.execute("SHOW TABLES")

events_check = 0
users_check = 0
for x in cur:
    if x[0] == "Events":
        events_check = 1
    print(x[0])

if events_check:
    print("Events database exists.")
else:
    cur.execute('''CREATE TABLE Events(
          id INT PRIMARY KEY auto_increment,
          sport VARCHAR(15),
          people_participating INT,
          people_needed INT,
          date_time VARCHAR(50),
          location VARCHAR(150),
          price FLOAT,
          description VARCHAR(300))
        ''')