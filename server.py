from flask import Flask, render_template, redirect, url_for, session, g
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Regexp, ValidationError, EqualTo
from flask_login import LoginManager, login_user, UserMixin, logout_user, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.app_context().push()
app.config["SECRET_KEY"] = "nothingmuch"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user-data-collection.db"
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
        self.admin_message = "Admin login is at /admin-login"

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
                raise ValidationError("Admin login at /admin-login")


user_check = User_check


class Pass_check(object):
    def __init__(self):
        self.error_message = "Incorrect Password"

    def __call__(self, form, field):
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password, field.data):
            raise ValidationError("Password Incorrect")


pass_check = Pass_check


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


##### DATABASE TABLESS


## USER TABLE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


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
    seats_available = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.String(30), unique=False, nullable=False)
    destination = db.Column(db.String(30), unique=False, nullable=False)


db.create_all()


### ROUTE CONFIGURATION


@app.route("/")
def home():
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
            password = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=1
            )
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


@app.route("/dashboard")
def dashboard_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            return redirect(url_for("admin_dashboard_page"))
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login_page"))


@app.route("/admin-dashboard")
def admin_dashboard_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            return render_template("admin-dashboard.html")
        return redirect(url_for("dashboard_page"))
    return redirect(url_for("login_page"))


@app.route("/flight-booking")
def flights_booking_page():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            return redirect(url_for("admin_dashboard_page"))
        return render_template("flight-booking.html")
    else:
        return redirect(url_for("login_page"))


@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
