from flask import Flask


app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>[+]Flask Application is up and running!</h1>"

if __name__ == "__main__":
    app.run(debug=True)