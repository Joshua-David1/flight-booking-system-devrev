from typing import Any
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    g,
    jsonify,
    request,
)
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Regexp, ValidationError, EqualTo
from flask_login import LoginManager, login_user, UserMixin, logout_user, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flight_process import FlightProcess
from booking_process import BookingProcess
from decouple import config

app = Flask(__name__)
app.app_context().push()
app.config["SECRET_KEY"] = "nothingmuch"
app.config["SQLALCHEMY_DATABASE_URI"] = config(
    "DATABASE_URL", "sqlite:///user-data-collection.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "OFF"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=10)
    session.modified = True
    g.user = current_user


### VALIDATIONS


class User_check(object):
    def __init__(self, register=False, admin=False):
        self.register = register
        self.admin = admin
        self.login_message = "user unavailable"
        self.register_message = "user already exists"
        self.admin_message = "Admin login is at '/admin-login'"

    def __call__(self, form, field):
        if self.register:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError(self.register_message)
        else:
            user = User.query.filter_by(username=field.data).first()
            if user == None:
                raise ValidationError(self.login_message)
            if user.username == "admin" and not self.admin:
                raise ValidationError(self.admin_message)

            if user.username != "admin" and self.admin:
                raise ValidationError("[!]Regular user not permitted")


user_check = User_check


class Pass_check(object):
    def __init__(self):
        self.error_message = "Incorrect Password"

    def __call__(self, form, field):
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.password != field.data:
            raise ValidationError("Password Incorrect")


pass_check = Pass_check


class SeatsCheck(object):
    def __init__(self):
        pass

    def __call__(self, form, field):
        if field.data is None or field.data == "":
            return

        if field.data.isnumeric() == False:
            return

        if int(field.data) < 60 or int(field.data) > 340:
            raise ValidationError("Seats must be between 60 and 340")


class MonthDayCheck(object):
    def __init__(self) -> None:
        pass

    def __call__(self, form, field):
        if field.data.lower() == "month" or field.data.lower() == "day":
            raise ValidationError("[!]Choose a valid option")


class SourceDestinationChosen(object):
    def __call__(self, form, field):
        if field.data.lower() == "source" or field.data.lower() == "destination":
            raise ValidationError("[!]Choose proper Source and Destination")


class HourMinuteChosen(object):
    def __call__(self, form, field):
        if field.data.lower() == "hour" or field.data.lower() == "minute":
            raise ValidationError("[!]Please choose a valid option!")


class FlightExistingCheck(object):
    def __call__(self, form, field):
        flight_no = field.data
        if Flight.query.filter_by(flight_no=flight_no).first() is not None:
            raise ValidationError("[!]Flight Already Exists")


def min_char_check(form, field):
    if len(field.data) < 5:
        raise ValidationError("Minimum 5 characters required")


###  FORMS


class LoginForm(FlaskForm):
    username = StringField(
        "username",
        render_kw={"placeholder": "Username", "maxlength": 25},
        validators=[
            InputRequired(message="Enter username"),
            min_char_check,
            user_check(admin=False),
        ],
    )
    password = PasswordField(
        "password",
        render_kw={"placeholder": "Password", "maxlength": 20},
        validators=[
            InputRequired(message="Enter password"),
            min_char_check,
            pass_check(),
        ],
    )


class LoginFormAdmin(FlaskForm):
    username = StringField(
        "username",
        render_kw={"placeholder": "Username", "maxlength": 25},
        validators=[
            InputRequired(message="Enter username"),
            min_char_check,
            user_check(admin=True),
        ],
    )
    password = PasswordField(
        "password",
        render_kw={"placeholder": "Password", "maxlength": 20},
        validators=[
            InputRequired(message="Enter password"),
            min_char_check,
            pass_check(),
        ],
    )


class RegisterForm(FlaskForm):
    username = StringField(
        "username",
        render_kw={"placeholder": "Username", "maxlength": 25},
        validators=[
            InputRequired(message="Enter username"),
            min_char_check,
            Regexp("^[\w]*$", message="Only letter, numbers and underscore."),
            Regexp("^[a-z\_0-9]*$", message="Only small letters"),
            Regexp("^[a-z\_]+[a-z\_0-9]*$", message="Cannot begin with numbers"),
            user_check(register=True),
        ],
    )
    password = PasswordField(
        "password",
        render_kw={"placeholder": "Password", "maxlength": 20},
        validators=[
            InputRequired(message="Enter password"),
            min_char_check,
            EqualTo("confirm_password", message="Passwords must match"),
        ],
    )
    confirm_password = PasswordField(
        "confirm_password",
        render_kw={"placeholder": "Confirm Password", "maxlength": 20},
        validators=[
            InputRequired(message="Please confirm your password"),
            min_char_check,
        ],
    )


class FlightDetailsForm(FlaskForm):
    flight_no = StringField(
        "flight_no",
        render_kw={"placeholder": "Flight Number", "maxlength": 8},
        validators=[
            InputRequired(message="Enter flight no"),
            Regexp("^[\w]*$", message="Only numbers followed by letters."),
            Regexp("^[a-z\_0-9]*$", message="Only small letters"),
            Regexp("^[0-9]+[a-z\_0-9]*$", message="Cannot begin with letters"),
            FlightExistingCheck(),
        ],
    )
    total_seats = StringField(
        "total_seats",
        render_kw={"placeholder": "Total Seats (60)", "maxlength": 3},
        validators=[
            InputRequired(message="Enter Flight number!"),
            Regexp("^[0-9]+$", message="Only numbers"),
            SeatsCheck(),
        ],
    )
    months_list = [
        "Month",
        "JAN",
        "FEB",
        "MAR",
        "APRIL",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
    ]
    days_list = ["Day"]
    places = [
        "Andhra Pradhesh",
        "Tamil Nadu",
        "Kerala",
        "Karnataka",
        "Bihar",
        "Goa",
        "Haryana",
        "Himachal Pradesh",
        "Punjab",
        "Odisha",
        "Rajasthan",
        "Telangana",
        "Maharashtra",
        "Sikkim",
        "West Bengal",
        "Gujarat",
        "Assam",
    ]

    source_list = ["Source"] + places
    destination_list = ["Destination"] + places
    hour_list = ["Hours"] + [i for i in range(0, 23)]
    min_list = ["Minutes"] + [i for i in range(0, 60)]
    for i in range(1, 31):
        days_list.append(i)
    month = SelectField(
        label="month", choices=months_list, validators=[MonthDayCheck()]
    )
    day = SelectField(label="day", choices=days_list, validators=[MonthDayCheck()])
    hour = SelectField(label="hour", choices=hour_list, validators=[HourMinuteChosen()])
    minute = SelectField(
        label="minute", choices=min_list, validators=[HourMinuteChosen()]
    )
    source = SelectField(
        label="source", choices=source_list, validators=[SourceDestinationChosen()]
    )
    destination = SelectField(
        label="destination",
        choices=destination_list,
        validators=[SourceDestinationChosen()],
    )


class SearchFlightForm(FlaskForm):
    places = [
        "Andhra Pradhesh",
        "Tamil Nadu",
        "Kerala",
        "Karnataka",
        "Bihar",
        "Goa",
        "Haryana",
        "Himachal Pradesh",
        "Punjab",
        "Odisha",
        "Rajasthan",
        "Telangana",
        "Maharashtra",
        "Sikkim",
        "West Bengal",
        "Gujarat",
        "Assam",
    ]
    source = SelectField(
        label="source",
        choices=["Source"] + places,
        validators=[SourceDestinationChosen()],
    )
    destination = SelectField(
        label="destination",
        choices=["Destination"] + places,
        validators=[SourceDestinationChosen()],
    )


##### DATABASE TABLESS


## USER TABLE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)


## BOOKED FLIGHTS TABLE


class Booking(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    flight_no = db.Column(db.String(8), nullable=False)


## AVAILABLE FLIGHTS TABLE


class Flight(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_no = db.Column(db.String(8), unique=True, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    seats_occupied = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(30), unique=False, nullable=False)
    destination = db.Column(db.String(30), unique=False, nullable=False)


db.create_all()


### ROUTE CONFIGURATION


@app.route("/")
def home():
    if not current_user.is_authenticated:
        return render_template("home.html")
    return redirect(url_for("login_page"))


@app.route("/login", methods=["POST", "GET"])
def login_page():
    form = LoginForm()
    if not current_user.is_authenticated:
        if form.validate_on_submit():
            username = form.username.data
            user = User.query.filter_by(username=username).first()
            login_user(user)
            print(current_user.username)
            return redirect(url_for("dashboard_page"))
        return render_template("login.html", form=form)
    return redirect(url_for("dashboard_page"))


@app.route("/register", methods=["POST", "GET"])
def register_page():
    form = RegisterForm()
    if not current_user.is_authenticated:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("dashboard_page"))
        return render_template("register.html", form=form)
    return redirect(url_for("dashboard_page"))


@app.route("/admin-login", methods=["POST", "GET"])
def admin_login_page():
    form = LoginFormAdmin()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        login_user(user)
        return redirect(url_for("admin_dashboard_page"))
    return render_template("admin-login.html", form=form)


@app.route("/myBooking")
def dashboard_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            return redirect(url_for("admin_dashboard_page"))
        booked_flights = Booking.query.filter_by(username=current_user.username).all()
        tickets_list = [
            Flight.query.filter_by(flight_no=details.flight_no).first()
            for details in booked_flights
        ]
        return render_template(
            "dashboard.html",
            data={"username": current_user.username, "tickets_list": tickets_list},
        )
    else:
        return redirect(url_for("login_page"))


@app.route("/admin-dashboard")
def admin_dashboard_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            all_flights = Flight.query.all()
            return render_template("admin-dashboard.html", all_flights=all_flights)
        return redirect(url_for("dashboard_page"))
    return redirect(url_for("login_page"))


@app.route("/book-flight", methods=["GET", "POST"])
def booking_flight_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            return redirect(url_for("admin_dashboard_page"))
        all_flights = Flight.query.all()
        booked_flights = Booking.query.filter_by(username=current_user.username).all()
        tickets_list = [
            Flight.query.filter_by(flight_no=details.flight_no).first()
            for details in booked_flights
        ]
        temp = []
        for flight in all_flights:
            if (
                flight not in tickets_list
                and flight.total_seats > flight.seats_occupied
            ):
                temp.append(flight)
        all_flights = temp
        return render_template("book-flight.html", all_flights=all_flights)
    else:
        return redirect(url_for("login_page"))


@app.route("/booking-confirmation", methods=["POST"])
def booking_confirmation_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            return redirect(url_for("admin_dashboard_page"))

        flight_id = request.form["flight-id"]
        flightProcess = FlightProcess(db, Flight)
        flight_no = flightProcess.get_flight_no(flight_id)
        is_available = flightProcess.check_seat_and_update(flight_id=flight_id)
        if is_available:
            flightProcess.update_seat(flight_id)
        else:
            redirect(url_for("dashboard_page"))
        data = {"username": current_user.username, "flight_no": flight_no}
        bookingProcess = BookingProcess(db, Booking)
        bookingProcess.add_to_booking(data)
        return redirect(url_for("dashboard_page"))
    return redirect(url_for("login_page"))


month_map = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APRIL": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}


@app.route("/add-flight", methods=["POST", "GET"])
def add_flight_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            form = FlightDetailsForm()
            if form.validate_on_submit():
                flight_no = form.flight_no.data
                total_seats = int(form.total_seats.data)
                hour = int(form.hour.data)
                minute = int(form.minute.data)
                month = form.month.data
                day = int(form.day.data)
                source = form.source.data
                destination = form.destination.data
                data = {
                    "flight_no": flight_no,
                    "total_seats": total_seats,
                    "hour": hour,
                    "minute": minute,
                    "month": month_map[month],
                    "day": day,
                    "source": source,
                    "destination": destination,
                }
                flightProcess = FlightProcess(db, Flight)
                flightProcess.add_to_db(data)
                return redirect(url_for("admin_dashboard_page"))
            return render_template("add-flight.html", form=form)
        return redirect(url_for("dashboard_page"))
    return redirect(url_for("login_page"))


@app.route("/search-flight", methods=["GET", "POST"])
def search_flight_page():
    if current_user.is_authenticated:
        if current_user.username != "admin":
            form = SearchFlightForm()
            data = {"form": form, "flight_list": []}
            if form.validate_on_submit():
                source = form.source.data
                destination = form.destination.data
                flightProcess = FlightProcess(db, Flight)
                flight_list = flightProcess.search_by_src_n_dst(source, destination)
                data = {"form": form, "flight_list": flight_list}
                return render_template("search-flight.html", data=data)
            return render_template("search-flight.html", data=data)
    return redirect(url_for("admin_dashboard_page"))


@app.route("/show-users", methods=["POST"])
def show_users_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            flightProcess = FlightProcess(db, Flight)
            flight_no = flightProcess.get_flight_no(request.form["flight-id"])
            users = Booking.query.filter_by(flight_no=flight_no).all()
            usernames = [uname.username for uname in users]
            return jsonify({flight_no: usernames})
    return redirect(url_for("login_page"))


@app.route("/cancel-flight", methods=["POST"])
def cancel_flight_route():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            fid = request.form["flight-id"]
            flightProcess = FlightProcess(db, Flight)
            fligh_no = flightProcess.get_flight_no(fid)
            flightProcess.cancel_flight(fid)
            bookingProcess = BookingProcess(db, Booking)
            bookingProcess.delete_from_booking(fligh_no)
            return redirect(url_for("admin_dashboard_page"))
        return redirect(url_for("dashboard_page"))
    return redirect(url_for("login_page"))


@app.route("/cancel-booking", methods=["POST"])
def cancel_booking_page():
    if current_user.is_authenticated:
        if current_user.username != "admin":
            f_no = request.form["flight_no"]
            bookingProcess = BookingProcess(db, Booking)
            bookingProcess.delete_from_booking(f_no)
            flightProcess = FlightProcess(db, Flight)
            flightProcess.decrement_seat(f_no)
    return redirect(url_for("login_page"))


@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
