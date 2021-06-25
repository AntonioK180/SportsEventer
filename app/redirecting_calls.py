from app import app
from flask import render_template, request, redirect, url_for, session, flash
from flask_cors import cross_origin
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models.user import User
from models.event import Event


mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


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
        user = User(*values)
        user.create()
        token = serializer.dumps(user.email, salt='email-confirm-key')
        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)

        msg = Message('SportsEventer Registration', sender='sportseventer@gmail.com', recipients=[user.email])
        msg.body = "Please follow the link to confirm your account: " + confirm_url
        mail.send(msg)
        return redirect('/')


@app.route('/confirm/<token>')
def confirm_email(token):
    email = serializer.loads(token, salt="email-confirm-key", max_age=86400)

    user = User.get_user_by_email(email)

    user.confirmed = True

    user.confirm()
    app.logger.info("Successfully registered a new user!")

    return redirect('/login')


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
                if username.confirmed == 1:
                    session['loggedin'] = True
                    session['id'] = username.user_id
                    session['username'] = username.username
                    app.logger.info("Successfully logged in!")
                    return redirect('/')
                else:
                    app.logger.info('This account is not confirmed')
                    flash('This account is not confirmed')
                    return redirect('/login')

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



@app.route('/rest/events/join', methods=['GET', 'PUT'])
def REST_join_event():
    if 'event_id' in request.args:
        if 'user_id' in request.args:
            event = Event.find(request.args['event_id'])
            user = User.get_user_by_id(request.args['user_id'])
            owner = User.get_user_by_username(event.created_by)
            event_token = serializer.dumps(event.event_id, salt='event-key')
            user_token = serializer.dumps(user.user_id, salt='user-key')
            accept_request_url = url_for(
                'accept_request',
                event_token=event_token,
                user_token=user_token,
                _external=True)

            msg = Message('SportsEventer: Request', sender='sportseventer@gmail.com', recipients=[owner.email])
            msg.body = "There has been a request for your " + event.sport + " event by " + user.username + ". To accept the request follow: " + accept_request_url + " \nYou can contact with " + user.username + " at the following email: " + user.email + "."
            mail.send(msg)
            return redirect('/')

    response = app.response_class(status=200)
    return response

@app.route('/accept/<event_token>/<user_token>')
def accept_request(event_token, user_token):
    event_id = serializer.loads(event_token, salt='event-key', max_age=86400)
    event = Event.find(event_id)
    user_id = serializer.loads(user_token, salt='user-key', max_age=86400)
    user = User.get_user_by_id(user_id)
    event.add_user_to_event(user_id)
    msg = Message('SportsEventer: Request', sender='sportseventer@gmail.com', recipients = [user.email])
    msg.body = "You have been approved for " + event.created_by + "'s " + event.sport + " event."
    mail.send(msg)
    return redirect('/')
