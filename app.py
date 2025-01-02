from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

habits = {
    1: {"name": "Drink water", "frequency": "daily"},
    2: {"name": "Work out", "frequency": "weekly"}
}

@app.route("/habits", methods=["POST"])
def create_habit():
    # Get data from the request
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    name = data.get("name")
    frequency = data.get("frequency")
    
    # Validate input
    if not name or not frequency:
        return jsonify({"error": "Both 'name' and 'frequency' are required"}), 400
    
    # Generate a unique ID
    new_id = max(habits.keys(), default=0) + 1
    
    # Add the new habit to the dictionary
    habits[new_id] = {"name": name, "frequency": frequency}
    
    # Return the created habit
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

if __name__ == "__main__":
    app.run(debug=True)
