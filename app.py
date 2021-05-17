from flask import Flask, render_template, request, redirect, url_for, session, flash
import logging
from event import EventEncoder, Event
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
    eventsReceived = Event.get_filtered_events("football", None, None)
    for i in eventsReceived:
        print(i.event_id)
    if 'loggedin' in session:
        return render_template('home.html', loggedin=True, user_id=session['id'])
    else:
        return render_template('home.html', loggedin=False)


@app.route('/register', methods=['GET', 'POST'])
@cross_origin()
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


@app.route('/myProfile/editEvent', methods=['GET', 'POST'])
def editEvent():
    if request.method == 'GET':
        return render_template('testEditEvent.html', currentUser=session['username'])
    elif request.method == 'POST':
        if 'event_id' in request.args:
            event = Event.find(request.args['event_id'])
            if event.created_by != session['username']:
                print("YOU CANNOT EDIT OTHER EVENTS!")
            else:
                event.people_participating = request.form['participating']
                event.people_needed = request.form['needed']
                event.date = request.form['date']
                event.time = request.form['time']
                event.location = request.form['location']
                event.price = request.form['price']
                event.description = request.form['description']
                event.save()
        return redirect(url_for('home'))


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

@app.route('/rest/events/getjoined', methods=['GET'])
@cross_origin()
def REST_GetJoinedEvents():
    if 'user_id' in request.args:
        response = app.response_class(
            response = json.dumps(Event.get_joined_events(request.args['user_id']), indent=4, cls=EventEncoder),
            status = 200,
            mimetype = 'application/json'
        )
        return response

@app.route('/rest/events/getfiltered', methods=['GET'])
@cross_origin()
def REST_GetFilteredEvents():
        response = app.response_class(
            response = json.dumps(Event.get_filtered_events(request.args['sport'], request.args['minprice'], request.args['maxprice']), indent=4, cls=EventEncoder),
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


@app.route('/rest/events/join', methods=['GET', 'PUT'])
def REST_JoinEvent():
    if 'event_id' in request.args:
        if 'user_id' in request.args:
            event = Event.find(request.args['event_id'])
            event.addUserToEvent(request.args['user_id'])

    response = app.response_class(status = 200)
    return response


@app.route('/rest/users', methods=['GET'])
@cross_origin()
def REST_GetUsername():
    if 'username' in request.args:
        print('THERE IS A USERNAME')
        if User.get_user_by_username(request.args['username']) is None:
            response = app.response_class(
                response = json.dumps({"nameFree":1}),
                status = 200,
                mimetype = 'application/json'
            )
            return response
        else:
            response = app.response_class(
                response = json.dumps({"nameFree":0}),
                status = 200,
                mimetype = 'application/json'
            )
            return response



if __name__ == '__main__':
    app.run(debug=True)
