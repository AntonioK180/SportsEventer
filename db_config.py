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