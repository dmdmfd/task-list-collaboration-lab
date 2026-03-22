from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

tasks = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    if not data or "task" not in data or not data["task"].strip():
        return jsonify({"error": "Task name required"}), 400

    task = {
        "id": len(tasks) + 1,
        "task": data["task"].strip(),
        "due_date": data.get("due_date", ""),
        "priority": data.get("priority", "Low"),
        "completed": False
    }

    tasks.append(task)
    return jsonify(task), 201


@app.route('/tasks/search', methods=['GET'])
def search_tasks():
    keyword = request.args.get("keyword", "").strip().lower()

    if not keyword:
        return jsonify(tasks)

    results = [
        task for task in tasks
        if keyword in task["task"].lower()
    ]

    return jsonify(results)


@app.route('/tasks/<int:id>/complete', methods=['PUT'])
def complete_task(id):
    for task in tasks:
        if task["id"] == id:
            task["completed"] = not task["completed"]
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    original_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != id]

    if len(tasks) == original_length:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)