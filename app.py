from flask import Flask, render_template, request, redirect, url_for, session, flash
import logging
from event import Event
from user import User


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
app.config['SECRET_KEY'] = 'bigsecreet'


@app.route('/')
def home():
    app.logger.info("Running...")
    if 'loggedin' in session:
        return render_template('home.html', events=Event.all(), loggedin=True)
    return render_template('home.html', events=Event.all(), loggedin=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['email'],
            request.form['username'],
            User.hash_password(request.form['pwd'])
        )
        User(*values).create()
        app.logger.info("Successfully registered a new user!")
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user = request.form['user']
        pwd = request.form['pwd']
        username = User.get_user_by_username(user)
        email = User.get_user_by_email(user)
        if username is not None:
            if username.verify_password(pwd) is True:
                session['loggedin'] = True
                session['id'] = username.user_id
                session['username'] = username.username
                app.logger.info("Successfully logged in!")
                return redirect('/')
            else:
                app.logger.info("Incorrect password!")
                flash("This is an incorrect password!")
                return redirect('/login')
        elif email is not None:
            if email.verify_password(pwd) is True:
                session['loggedin'] = True
                session['id'] = username.id
                session['username'] = username.username
                app.logger.info("Successfully logged in!")
                return redirect('/')
            else:
                app.logger.info("Wrong password!")
                return redirect('/login')
        else:
            flash("Incorrect username!")
            return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/myProfile')
def myProfile():
    currentUser = User.get_user_by_username(session['username'])
    return render_template('myProfile.html', user=currentUser)


@app.route('/newEvent', methods=['GET', 'POST'])
def newEvent():
    if request.method == 'GET':

        return render_template('newEvent.html')
    elif request.method == 'POST':
        sport = request.form['sport']
        people_participating = request.form['people_participating']
        people_needed = request.form['people_needed']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        price = request.form['price']
        description = request.form['description']

        new_event = Event(None, session['username'], sport, people_participating,
                          people_needed, date, time, location, price, description)
        new_event.create()
        return redirect('/')


@app.route('/events/<int:event_id>')
def openEvent(event_id):
    event = Event.find(event_id)

    return render_template('event.html', event=event), 200


@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def editEvent(event_id):
    event = Event.find(event_id)
    if request.method == 'GET':

        return render_template('edit_event.html', event=event)
    elif request.method == 'POST':
        if event.created_by == session['username']:
            event.people_participating = request.form['people_participating']
            event.people_needed = request.form['people_needed']
            event.date = request.form['date']
            event.time = request.form['time']
            event.location = request.form['location']
            event.price = request.form['price']
            event.description = request.form['description']
            event.save()

            return redirect(url_for('openEvent', event_id=event.event_id))
        else:
            print("You can't edit others' events!")
            return redirect('/')


@app.route('/events/<int:event_id>/delete', methods=['POST'])
def deleteEvent(event_id):
    event = Event.find(event_id)
    if event.created_by == session['username']:
        event.delete()
    else:
        print("You can't delete others' events!")
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
