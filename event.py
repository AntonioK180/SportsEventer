from db_config import mydb
from json import JSONEncoder


cur = mydb.cursor(buffered=True)


class Event():
    def __init__(self, event_id, created_by, sport, people_participating, people_needed, date, time, location, price, description):
        self.event_id = event_id
        self.created_by = created_by
        self.sport = sport
        self.people_participating = people_participating
        self.people_needed = people_needed
        self.date = date
        self.time = time
        self.location = location
        self.price = price
        self.description = description


    @staticmethod
    def all():
        cur.execute("SELECT * FROM Events")
        result = cur.fetchall()
        return [Event(*row) for row in result]


    @staticmethod
    def find(event_id):
        query = "SELECT * FROM Events WHERE event_id = %s"
        value = (event_id,)
        cur.execute(query, value)
        row = cur.fetchone()
        if row is None:
            return
        return Event(*row)


    @staticmethod
    def findByUsername(created_by):
        query = "SELECT * FROM Events WHERE created_by = %s"
        value = (created_by,)
        cur.execute(query, value)
        result = cur.fetchall()
        if result is None:
            return
        return [Event(*row) for row in result]

    @staticmethod
    def get_joined_events(user_id):
        query = 'SELECT event_id FROM UsersEvents WHERE user_id=%s'
        value = (user_id,)
        print(user_id)
        cur.execute(query, value)
        results = cur.fetchall()
        events = []
        if results is None:
            return;
        else:
            for row in results:
                events.append(Event.find(*row))
            if len(events) == 0:
                return;
            else:
                return events

    @staticmethod
    def get_filtered_events(sport, min_price, max_price):
        print("In the function")
        start_query = 'SELECT * FROM Events WHERE '
        and_query = ' AND '
        if sport != "All sports":
            print("In the sports if")
            sport_query = 'sport = "' + sport + '"'
            print(sport_query)
        else:
            sport_value = ('sport IS NOT NULL')
        if min_price is not None and max_price is not None:
            price_query = 'price BETWEEN ' + str(min_price) + ' AND ' + str(max_price)
        elif min_price is not None and max_price is None:
            price_query = 'price >= ' + str(min_price)
        elif min_price is None and max_price is not None:
            price_query = 'price <= ' + str(max_price)
        else:
            price_query = ('price IS NOT NULL')
        print("Outside ifs")
        query = start_query + sport_query + and_query + price_query
        print(query)
        print("After the tuple")
        cur.execute(query)
        print("After the execute")
        result = cur.fetchall()
        print("After the fetch")
        if result is None:
            return
        return [Event(*row) for row in result]




    def create(self):
        query = "INSERT INTO Events (sport, created_by, people_participating, people_needed, event_date, event_time, location, price, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        value = (self.sport, self.created_by, self.people_participating, self.people_needed,
                 self.date, self.time, self.location, self.price, self.description)
        cur.execute(query, value)
        mydb.commit()


    def save(self):
        query = "UPDATE Events SET people_participating = %s, people_needed = %s, event_date = %s, event_time = %s, location = %s, price = %s, description = %s WHERE event_id = %s"
        value = (self.people_participating, self.people_needed, self.date, self.time,
                 self.location, self.price, self.description, self.event_id)
        cur.execute(query, value)
        mydb.commit()


    def delete(self):
        query = "DELETE FROM Events WHERE event_id = %s"
        value = (self.event_id,)
        cur.execute(query, value)
        mydb.commit()


    def addUserToEvent(self, user_id):
        query = "INSERT INTO UsersEvents(event_id, user_id) VALUES(%s, %s)"
        value = (self.event_id, user_id)
        cur.execute(query, value)
        mydb.commit()
        self.people_participating += 1
        self.save()




class EventEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
