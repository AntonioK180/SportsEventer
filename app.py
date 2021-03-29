from flask import Flask, render_template, request, redirect, url_for
import logging
from event import Event


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', events=Event.all())

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


@app.route('/events/<int:event_id>')
def openEvent(event_id):
    event = Event.find(event_id)

    return render_template('event.html', event = event)


@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.find(event_id)
    if request.method == 'GET':

        return render_template('edit_event.html' , event = event)
    elif request.method == 'POST':
        event.sport = request.form['sport']
        event.people_participating = request.form['people_participating']
        event.people_needed = request.form['people_needed']
        event.date_time = request.form['date_time']
        event.location = request.form['location']
        event.price = request.form['price']
        event.description = request.form['description']
        event.save()

        return redirect(url_for('openEvent', event_id = event.event_id))

if __name__ == '__main__':
    app.run(debug=True)
