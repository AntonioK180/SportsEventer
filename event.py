from db_config import mydb


cur = mydb.cursor()


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
