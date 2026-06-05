from flask import Flask, jsonify, request
from app.services import TaskService

app = Flask(__name__)
task_service = TaskService()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(task_service.get_all_tasks())

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'title required'}), 400
    task = task_service.create_task(data['title'])
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    task = task_service.update_task(task_id, request.get_json().get('done'))
    if not task:
        return jsonify({'error': 'not found'}), 404
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not task_service.delete_task(task_id):
        return jsonify({'error': 'not found'}), 404
    return '', 204
