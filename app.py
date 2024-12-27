from flask import Flask 
import json
app = Flask (__name__)

@app.route("/")
def home():
	return "Hello, World!"
if __name__ == "__main__":
	app.run(debug=True)

habits = {
	1: {"name":"Drink water", "frequency" : "daily"},
	2: {"name": "Work out", "frequency": "weekly"}
}

@app.route ("/habits", methods = ["POST"])
def create_habit():
	data = request.json
	name =data.get("name")
	frequency = data.get("frequency")
	if not name or not frequency:
		return jsonify({"error": "Both 'name' and 'frequency' are required"}), 400
