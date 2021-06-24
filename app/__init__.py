from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = 'bigsecreet'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sportseventer@gmail.com'
app.config['MAIL_PASSWORD'] = 'iskamkni6ka'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

from app import rest_calls
from app import redirecting_calls
from app import error_handling
