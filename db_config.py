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
users_events_check = 0
for x in cur:
    if x[0] == "Events":
        events_check = 1
    if x[0] == "Users":
        users_check = 1
    if x[0] == "UsersEvents":
        users_events_check = 1
    print(x[0])

if events_check:
    print("Events table exists.")
else:
    cur.execute('''CREATE TABLE Events(
          event_id             INT PRIMARY KEY auto_increment,
          created_by           VARCHAR(40) NOT NULL,
          sport                VARCHAR(15),
          people_participating INT,
          people_needed        INT,
          event_date           VARCHAR(50),
          event_time           VARCHAR(30),
          location             VARCHAR(150),
          price                FLOAT,
          description          VARCHAR(300));
        ''')

if users_check:
    print("Users table exists.")
else:
    cur.execute('''CREATE TABLE Users(
         user_id          INT PRIMARY KEY NOT NULL auto_increment,
         email            VARCHAR(60) NOT NULL,
         username         VARCHAR(40) NOT NULL,
         pwd              VARCHAR(300) NOT NULL);
       ''')

if users_events_check:
    print("UsersEvents table exists.")
else:
    cur.execute('''CREATE TABLE UsersEvents(
        id          INT PRIMARY KEY NOT NULL auto_increment,
        event_id    INT NOT NULL,
        FOREIGN KEY(event_id) REFERENCES Events(event_id),
        user_id     INT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES Users(user_id));
       ''')
