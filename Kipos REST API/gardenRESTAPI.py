#This is a simple gardening API using Flask, SQLite, and MArshmellow
#

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Set up the Flask app and database
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "gardening.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define the Plant model
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(100))
    watering_frequency = db.Column(db.String(100))
    last_watered = db.Column(db.DateTime)

# Define the Plant schema
class PlantSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "type", "watering_frequency", "last_watered")

# Initialize the Plant schema
plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)

# Set up the API endpoints

# Get a list of all plants
@app.route("/plants", methods=["GET"])
def get_plants():
    all_plants = Plant.query.all()
    result = plants_schema.dump(all_plants)
    return jsonify(result)

# Get a single plant by ID
@app.route("/plant/<id>", methods=["GET"])
def get_plant(id):
    plant = Plant.query.get(id)
    result = plant_schema.dump(plant)
    return jsonify(result)

# Add a new plant
@app.route("/plant", methods=["POST"])
def add_plant():
    name = request.json["name"]
    type = request.json["type"]
    watering_frequency = request.json["watering_frequency"]
    last_watered = request.json["last_watered"]

    new_plant = Plant(name=name, type=type, watering_frequency=watering_frequency, last_watered=last_watered)
    db.session.add(new_plant)
    db.session.commit()

    plant = Plant.query.get(new_plant.id)
    result = plant_schema.dump(plant)
    return jsonify(result)

# Update an existing plant by ID
@app.route("/plant/<id>", methods=["PUT"])
def update_plant(id):
    plant = Plant.query.get(id)

    name = request.json["name"]
    type = request.json["type"]
    watering_frequency = request.json["watering_frequency"]
    last_watered = request.json["last_watered"]

    plant.name = name
    plant.type = type
    plant.watering_frequency = watering_frequency
    plant.last_watered = last_watered

    db.session.commit()
    result = plant_schema.dump(plant)
    return jsonify(result)

# Delete a plant by ID
@app.route("/plant/<id>", methods=["DELETE"])
def delete_plant(id):
    plant = Plant.query.get(id)
    db.session.delete(plant)
    db.session.commit()
    return jsonify("Plant deleted")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
