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
def my_profile():
    currentUser = User.get_user_by_username(session['username'])

    return render_template('myProfile.html', user=currentUser)


@app.route('/myProfile/<int:user_id>/edit')
def edit_profile():

    return render_template('editProfile.html')


@app.route('/newEvent', methods=['GET', 'POST'])
def new_event():
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

        event = Event(None, session['username'], sport, people_participating,
                      people_needed, date, time, location, price, description)
        event.create()
        return redirect('/')


@app.route('/myProfile/editEvent', methods=['GET', 'POST'])
def edit_event():
    if request.method == 'GET':
        return render_template('editEvent.html', currentUser=session['username'])
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
def REST_get_events():
    if 'user_id' in request.args:
        user = User.get_user_by_id(request.args['user_id'])
        response = app.response_class(
            response=json.dumps(Event.find_by_username(user.username), indent=4, cls=EventEncoder),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps(Event.all(), indent=4, cls=EventEncoder),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route('/rest/events/getjoined', methods=['GET'])
@cross_origin()
def REST_get_joined_events():
    if 'user_id' in request.args:
        response = app.response_class(
            response=json.dumps(Event.get_joined_events(request.args['user_id']), indent=4, cls=EventEncoder),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/rest/events/getfiltered', methods=['GET'])
@cross_origin()
def REST_get_filtered_events():
    sport = None
    minprice = None
    maxprice = None

    if 'sport' in request.args:
        if request.args['sport'] != "all":
            sport = request.args['sport']

    if 'minprice' in request.args:
        minprice = request.args['minprice']

    if 'maxprice' in request.args:
        maxprice = request.args['maxprice']

    response = app.response_class(
        response=json.dumps(Event.get_filtered_events(sport, minprice, maxprice), indent=4, cls=EventEncoder),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/rest/events/delete', methods=['DELETE'])
def REST_delete_event():
    if 'event_id' in request.args:
        event = Event.find(request.args['event_id'])
        event.delete()
        response = app.response_class(status=200)
        return response


@app.route('/rest/events/edit', methods=['GET', 'POST'])
def REST_edit_event():
    if 'event_id' in request.args:
        if request.method == 'GET':
            event = Event.find(request.args['event_id'])
            response = app.response_class(
                response=json.dumps(event, indent=4, cls=EventEncoder),
                status=200,
                mimetype='application/json'
            )
            return response
        elif request.method == 'POST':
            data = request.get_json(force=True)


@app.route('/rest/events/join', methods=['GET', 'PUT'])
def REST_join_event():
    if 'event_id' in request.args:
        if 'user_id' in request.args:
            event = Event.find(request.args['event_id'])
            event.add_user_to_event(request.args['user_id'])

    response = app.response_class(status=200)
    return response


@app.route('/rest/users', methods=['GET'])
@cross_origin()
def REST_get_username():
    if 'username' in request.args:
        print('THERE IS A USERNAME')
        if User.get_user_by_username(request.args['username']) is None:
            response = app.response_class(
                response=json.dumps({"nameFree": 1}),
                status=200,
                mimetype='application/json'
            )
            return response
        else:
            response = app.response_class(
                response=json.dumps({"nameFree": 0}),
                status=200,
                mimetype='application/json'
            )
            return response


if __name__ == '__main__':
    app.run(debug=True)
