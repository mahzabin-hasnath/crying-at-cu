from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

### DATABASE ###
app.config['SECRET_KEY'] = 'issasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pin(db.Model):
    pin_id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    place = db.Column(db.Text, nullable=False)
    def __init__(self, lat, long, reason, place):
        self.lat = lat
        self.long = long
        self.reason = reason
        self.place = place


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pindata')
def pindata():
    pins = Pin.query.all()
    data = [[pin.lat, pin.long, pin.reason, pin.place] for pin in pins]
    return jsonify({"data": data})

@app.route('/addpin', methods=['GET', 'POST'])
def addpin():
    if request.method == 'POST':
        data = request.get_json()
        pin = Pin(data["latitude"], data["longitude"], data["reason"], data["place"])
        db.session.add(pin)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("addpin.html")
