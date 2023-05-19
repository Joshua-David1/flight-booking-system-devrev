from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Regexp, ValidationError

app = Flask(__name__)
app.config["SECRET_KEY"] = "nothingmuch"


def min_char_check(form, field):
    if len(field.data) < 6:
        raise ValidationError("Minimum 6 characters required")


class LoginForm(FlaskForm):
    username = StringField(
        "username",
        render_kw={"placeholder": "Username", "maxlength": 25},
        validators=[InputRequired(message="Enter username"), min_char_check],
    )
    password = PasswordField(
        "password",
        render_kw={"placeholder": "Password", "maxlength": 20},
        validators=[InputRequired(message="Enter password"), min_char_check],
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
        ],
    )
    password = PasswordField(
        "password",
        render_kw={"placeholder": "Password", "maxlength": 20},
        validators=[InputRequired(message="Enter password"), min_char_check],
    )
    confirm_password = PasswordField(
        "confirm_password",
        render_kw={"placeholder": "Confirm Password", "maxlength": 20},
        validators=[
            InputRequired(message="Please confirm your password"),
            min_char_check,
        ],
    )


@app.route("/")
def home():
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/register")
def register_page():
    form = RegisterForm()
    return render_template("register.html", form=form)


@app.route("/dashboard")
def tickets_page():
    return render_template("dashboard.html")


@app.route("/flight-booking")
def flights_booking_page():
    return ""


if __name__ == "__main__":
    app.run(debug=True)
