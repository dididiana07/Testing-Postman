import random
from flask import Flask, jsonify, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

def serialize(coffee):
    cafe_dictionary = {
        "id": coffee.id,
        "name": coffee.name,
        "map_url": coffee.map_url,
        "img_url": coffee.img_url,
        "location": coffee.location,
        "seats": coffee.seats,
        "has_toilet": coffee.has_toilet,
        "has_wifi": coffee.has_wifi,
        "has_sockets": coffee.has_sockets,
        "can_take_calls": coffee.can_take_calls,
        "coffee_price": coffee.coffee_price
    }
    return cafe_dictionary


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record

@app.route("/random", methods=["GET"])
def random_cafe():
    cafes = len(Cafe.query.all()) - 1
    id_cafe = random.randint(0, cafes)
    chosen_cafe = Cafe.query.filter_by(id=id_cafe).first()
    return jsonify(serialize(chosen_cafe))


@app.route("/all", methods=["GET"])
def all_database():
    all_coffees = Cafe.query.all()
    return jsonify([serialize(coffee) for coffee in all_coffees])


@app.route("/search", methods=["GET"])
def find_location():
    location = request.args["loc"]
    if "-" in location:
        location = " ".join(location.split("-"))
    location = location.title()
    all_locations = Cafe.query.filter_by(location=location).all()
    if len(all_locations) == 0:
        return jsonify("error")
    return jsonify([serialize(location) for location in all_locations])

# HTTP POST - Create Record

@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    name = request.args["name"]
    location = request.args["loc"]
    map_url = request.args["map_url"]
    img_url = request.args["img_url"]
    seats = request.args["seats"]
    has_toilet = bool(request.args["has_toilet"])
    has_sockets = bool(request.args["has_sockets"])
    has_wifi = bool(request.args["has_wifi"])
    can_take_calls = bool(request.args["can_take_calls"])
    coffee_price = request.args["coffee_price"]
    new_coffee = Cafe(name=name,
                      location=location,
                      map_url=map_url,
                      img_url=img_url,
                      seats=seats,
                      has_toilet=has_toilet,
                      has_wifi=has_wifi,
                      has_sockets=has_sockets,
                      can_take_calls=can_take_calls,
                      coffee_price=coffee_price)
    db.session.add(new_coffee)
    db.session.commit()
    return jsonify([{"response":"Successfully added to the database."}])

# HTTP PUT/PATCH - Update Record

@app.route("/update-cafe", methods=["PATCH"])
def update_price():
    id_coffee = request.args["id_coffee"]
    new_price = request.args["price"]
    coffee_to_update = Cafe.query.filter_by(id=id_coffee).first()
    coffee_to_update.coffee_price = new_price
    db.session.commit()
    return jsonify([{"Response":"Successfully updated price."}])

# HTTP DELETE - Delete Record

@app.route("/delete-cafe", methods=["DELETE"])
def delete_cafe():
    id_cafe = request.args["id_coffee"]
    apiKey = request.args["TopSecretAPIKey"]
    if apiKey != "DidiLovesCoding23#":
        return jsonify([{"Response": "Wrong API Key method not allowed."}])
    else:
        coffee_to_delete = Cafe.query.filter_by(id=id_cafe).first()
        if not coffee_to_delete:
            return jsonify([{"Response":"Sorry we haven't located the coffee store."}])
        else:
            db.session.delete(coffee_to_delete)
            db.session.commit()
            return jsonify([{"Response":"Successfully deleted."}])



if __name__ == '__main__':
    app.run(debug=True)
