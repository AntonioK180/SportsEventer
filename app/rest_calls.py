from app import app
from flask import request
from models.event import EventEncoder, Event
from models.user import User
import json
from flask_cors import cross_origin


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
