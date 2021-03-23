from flask import Flask, render_template, request
import logging
from event import Event


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/newEvent', methods=['GET', 'POST'])
def newEvent():
    if request.method == 'POST':
        sport = request.form['sport']
        people_participating = request.form['people_participating']
        people_needed = request.form['people_needed']
        date_time = request.form['date_time']
        location = request.form['location']
        price = request.form['price']
        description = request.form['description']

        new_event = Event(None, sport, people_participating, people_needed, date_time, location, price, description)
        new_event.create()
    return render_template('newEvent.html')

if __name__ == '__main__':
    app.run(debug=True)
