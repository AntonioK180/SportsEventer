from db_config import mydb


cur = mydb.cursor()


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
        cur.execute("SELECT * FROM Events")
        result = cur.fetchall()
        return [Event(*row) for row in result]

    @staticmethod
    def find(event_id):
        query = "SELECT * FROM Events WHERE id = %s"
        value = (event_id,)
        cur.execute(query, value)
        row = cur.fetchone()
        if row is None:
            return
        return Event(*row)

    def create(self):
        query = "INSERT INTO Events (sport, people_participating, people_needed, date_time, location, price, description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        value = (self.sport, self.people_participating, self.people_needed,
                 self.date_time, self.location, self.price, self.description)
        cur.execute(query, value)
        mydb.commit()

    def save(self):
        query = "UPDATE Events SET people_participating = %s, people_needed = %s, date_time = %s, location = %s, price = %s, description = %s WHERE id = %s"
        value = (self.people_participating, self.people_needed, self.date_time,
                 self.location, self.price, self.description, self.event_id)
        cur.execute(query, value)
        mydb.commit()

    def delete(self):
        query = "DELETE FROM Events WHERE id = %s"
        value = (self.event_id,)
        cur.execute(query, value)
        mydb.commit()
