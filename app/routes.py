from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_id = 1  # at top of file, outside everything

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'title required'}), 400
    task = {'id': next_id, 'title': data['title'], 'done': False}
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'not found'}), 404
    task['done'] = request.get_json().get('done', task['done'])
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'not found'}), 404
    tasks.remove(task)
    return '', 204
