class FlightProcess(object):
    def __init__(self, db, Flight):
        self.data = None
        self.db = db
        self.flight = Flight

    def add_to_db(self, data):
        self.data = data
        flight_no = self.data["flight_no"]
        total_seats = self.data["total_seats"]
        seats_occupied = 0
        hour = self.data["hour"]
        minute = self.data["minute"]
        day = self.data["day"]
        month = self.data["month"]
        source = self.data["source"]
        destination = self.data["destination"]
        new_flight = self.flight(
            flight_no=flight_no,
            total_seats=total_seats,
            seats_occupied=seats_occupied,
            hour=hour,
            minute=minute,
            day=day,
            month=month,
            source=source,
            destination=destination,
        )
        self.db.session.add(new_flight)
        self.db.session.commit()

    def cancel_flight(self, flight_id):
        self.db.session.delete(self.flight.query.filter_by(id=flight_id).first())
        self.db.session.commit()

    def get_flight_no(self, flight_id):
        return self.flight.query.filter_by(id=flight_id).first().flight_no

    def check_seat_and_update(self, flight_id):
        flight = self.flight.query.filter_by(id=flight_id).first()
        if flight.total_seats - flight.seats_occupied > 0:
            return 1
        return 0

    def update_seat(self, flight_id):
        flight = self.flight.query.filter_by(id=flight_id).first()
        flight.seats_occupied += 1
        self.db.session.commit()

    def decrement_seat(self, flight_no):
        flight = self.flight.query.filter_by(flight_no=flight_no).first()
        flight.seats_occupied -= 1
        self.db.session.commit()

    def search_by_src_n_dst(self, source, destination):
        flight = self.flight.query.filter_by(
            source=source, destination=destination
        ).all()
        temp = []
        for f in flight:
            if f.total_seats > f.seats_occupied:
                temp.append(f)
        return temp
