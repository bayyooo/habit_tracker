from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
today = date.today()
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bayleyosornio@localhost/bayleyosornio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Habit(db.Model):
    __tablename__ = 'habit'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    habit_name = db.Column(db.String(100), unique=True, nullable=False)  # Unique name
    description = db.Column(db.String(250)) 
    date = db.Column(db.Date, default=date.today)
    status=db.Column(db.Boolean, default=False)
    

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    email=db.Column(db.String(250), unique=True, nullable=False)  # Unique email
    password=db.Column(db.Text, nullable=False)  # Password
    habits = db.relationship('Habit', backref='user', lazy=True)

class Tracking(db.Model):
    __tablename__ = 'tracking'
    id=db.Column(db.Integer, primary_key=True)  # Primary Key
    habit_id=db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, default=date.today)

class DaysOfWeek(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class Frequency(db.Model):
    __tablename__ = 'frequency'
    id =db.Column(db.Integer, primary_key=True)  # Primary Key
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    days = db.Column(db.Enum(DaysOfWeek), nullable=False)  # Enum for days of the week

    def __repr__(self):
        return f'<habit_id {self.habit_name}>'





@app.route("/")
def home():
    return "Hello, World!"

habits = {
    1: {"name": "Drink water", "frequency": "daily", "streak": 5, "last_completed": "2021-01-01"},
    2: {"name": "Work out", "frequency": "weekly", "streak": 0, "last_completed": None},
}

@app.route("/habits", methods=["POST"])
def create_habit():

    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    name = data.get("name")
    frequency = data.get("frequency")
    streak = data.get("streak", 0)
    last_completed = data.get("last_completed", None)

    if not name or not frequency:
        return jsonify({"error": "Both 'name' and 'frequency' are required"}), 400
    new_id = max(habits.keys(), default=0) + 1
    habits[new_id] = {"name": name, "frequency": frequency}
    return jsonify({"id": new_id, "name": name, "frequency": frequency}), 201

@app.route("/habits/<int:id>", methods=["GET"])
def read_habit(id):
    habit = habits.get(id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
    return jsonify(habit), 200


@app.route("/habits/<int:id>", methods=["DELETE"])
def delete_habit(id):
    if id not in habits:
        return jsonify({"error": "Habit not found"}), 404
    deleted_habit = habits.pop(id)
    return jsonify({"message": "Habit deleted", "habit": deleted_habit}), 200

@app.route("/habits/<int:id>", methods=["PUT"])
def update_habit(id):
    if id not in habits:
        return jsonify({"error": "Habit not found"}), 404
    
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    name = data.get("name", habits[id]["name"])
    frequency = data.get("frequency", habits[id]["frequency"])
    
    habits[id].update({"name": name, "frequency": frequency})
    return jsonify({"message": "Habit updated", "habit": habits[id]}), 200

@app.route("/habits/<int:id>/complete", methods=["POST"])
def complete_habit(id):
    if id not in habits:
        return jsonify({"error": "Habit not found"}), 404
        last_completed_date = date.fromisoformat(last_completed)
        


if __name__ == "__main__":
    app.run(debug=True)
