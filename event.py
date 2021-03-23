from db_config import mydb


class Event():
    def __init__(self, event_id, sport, people_participating, people_needed, date_time, location, price, description):
        self.event_id = event_id
        self.sport = sport
        self.people_participating = people_participating
        self.people_needed = people_needed
        self.date_time = date_time
        self.location = location
        self.price = price
        self.description = description

    @staticmethod
    def all():
        cur = mydb.cursor()
        cur.execute("SELECT * FROM Events")
        result = cur.fetchall()
        return [Event(*row) for row in result]

    def create(self):
        cur = mydb.cursor()
        query = "INSERT INTO Events (sport, people_participating, people_needed, date_time, location, price, description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        value = (self.sport, self.people_participating, self.people_needed, self.date_time, self.location, self.price, self.description)
        cur.execute(query, value)
        mydb.commit()
