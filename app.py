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

    task = {
        "id": len(tasks) + 1,
        "task": data["task"]
    }

    tasks.append(task)
    return jsonify(task), 201

if __name__ == '__main__':
    app.run(debug=True)