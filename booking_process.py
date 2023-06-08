class BookingProcess(object):
    def __init__(self, db, Booking):
        self.db = db
        self.booking = Booking

    def add_to_booking(self, data):
        self.data = data
        username = self.data["username"]
        flight_no = self.data["flight_no"]
        self.db.session.add(self.booking(username=username, flight_no=flight_no))
        self.db.session.commit()

    def delete_from_booking(self, flight_no, admin=True, username=None):
        booked = self.booking.query.filter_by(flight_no=flight_no).all()
        if not admin:
            booked = self.booking.query.filter_by(
                flight_no=flight_no, username=username
            ).all()
        if booked is None or booked == []:
            return
        for b in booked:
            self.db.session.delete(b)
            self.db.session.commit()
