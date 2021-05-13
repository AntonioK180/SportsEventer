from flask import Flask, render_template, request, redirect, url_for, session, flash
import logging
from event import Event, EventEncoder
from user import User
import json
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
logging.basicConfig(level=logging.DEBUG)
app.config['SECRET_KEY'] = 'bigsecreet'

@app.route('/')
def home():
    app.logger.info("Running...")
    if 'loggedin' in session:
        return render_template('home.html', loggedin=True, user_id=session['id'])
    else:
        return render_template('home.html', loggedin=False)


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
@cross_origin()
def myProfile():
    currentUser = User.get_user_by_username(session['username'])

    return render_template('myProfile.html', user=currentUser)


@app.route('/myProfile/<int:user_id>/edit')
def editProfile(user_id):
    user = User.get_user_by_id(user_id)

    return render_template('editProfile.html')


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


@app.route('/rest/events', methods=['GET'])
@cross_origin()
def REST_GetEvents():
    if 'user_id' in request.args:
        user = User.get_user_by_id(request.args['user_id'])
        response = app.response_class(
            response = json.dumps(Event.findByUsername(user.username), indent=4, cls=EventEncoder),
            status = 200,
            mimetype = 'application/json'
        )
    else:
        response = app.response_class(
            response = json.dumps(Event.all(), indent=4, cls=EventEncoder),
            status = 200,
            mimetype = 'application/json'
        )
    return response


@app.route('/rest/events/delete', methods=['DELETE'])
def REST_DeleteEvent():
    if 'event_id' in request.args:
        event = Event.find(request.args['event_id'])
        event.delete()
        response = app.response_class(status=200)
        return response


@app.route('/rest/events/edit', methods=['GET', 'POST'])
def REST_EditEvent():
    if 'event_id' in request.args:
        if request.method == 'GET':
            event = Event.find(request.args['event_id'])
            response = app.response_class(
                response = json.dumps(event, indent=4, cls=EventEncoder),
                status = 200,
                mimetype = 'application/json'
            )
            return response
        elif request.method == 'POST':
            data = request.get_json(force=True)
            print(data)


@app.route('/rest/events/join', methods=['GET', 'POST'])
def REST_JoinEvent():
    if 'event_id' in request.args:
        if 'loggedin' in session:
            event = Event.find(request.args['event_id'])
            event.addUserToEvent(session['id'])
        response = app.response_class(status = 200)

        return response


@app.route('/myProfile/editEvent', methods=['GET', 'POST'])
def editEvent():
    if request.method == 'GET':
        return render_template('testEditEvent.html')
    elif request.method == 'POST':
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
