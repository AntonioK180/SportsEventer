import yaml
import mysql.connector


db = yaml.load(open('db.yaml'))
mydb = mysql.connector.connect(
    host=db['mysql_host'],
    user=db['mysql_user'],
    password=db['mysql_password'],
    database="SportsEventer",
    auth_plugin='mysql_native_password'
)

cur = mydb.cursor()

cur.execute("SHOW TABLES")

events_check = 0
users_check = 0
for x in cur:
    if x[0] == "Events":
        events_check = 1
    if x[0] == "Users":
        users_check = 1
    print(x[0])

if events_check:
    print("Events table exists.")
else:
    cur.execute('''CREATE TABLE Events(
          event_id INT PRIMARY KEY auto_increment,
          created_by VARCHAR(40) NOT NULL,
          sport VARCHAR(15),
          people_participating INT,
          people_needed INT,
          date_time VARCHAR(50),
          location VARCHAR(150),
          price FLOAT,
          description VARCHAR(300));
        ''')

if users_check:
    print("Users table exists.")
else:
    cur.execute('''CREATE TABLE Users(
	   id int Primary Key not null auto_increment,
	   email tinytext not null,
	   username tinytext not null,
	   pwd tinytext not null);
       ''')
