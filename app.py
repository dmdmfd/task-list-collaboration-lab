from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"error": "Task name required"}), 400

    #Get and validate priority( defult to  "low"  if missing /invalid)

    priority = data.get("priority", "low").lower()
    if priority not in ("high", "medium", "low"):
        priority = "low"
 
    task = {
        "id": len(tasks) + 1,
        "task": data["task"],
        "priority": priority
    }

    tasks.append(task)
    return jsonify(task), 201

if __name__ == '__main__':
    app.run(debug=True)