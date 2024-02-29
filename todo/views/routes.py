from flask import Blueprint, jsonify, request, abort
from todo.models.todo import ToDoDatabaseHelper
api = Blueprint('api', __name__, url_prefix='/api/v1')
database = ToDoDatabaseHelper()

POST_RETURN_STATUS = 201

@api.route('/health')
def health():
    return jsonify({'status': 'ok'})

@api.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(database.get_all_todos())

@api.route('/todos/<int:id>', methods=['GET'])
def get_todo(id: int):
    todo_entry = database.get_todo_by_id(id)
    if todo_entry is not None:
        return jsonify(todo_entry)
    else:
        abort(404)

@api.route('/todos', methods=['POST'])
def create_todo():
    title = request.json.get('title')
    description = request.json.get('description')
    completed = request.json.get('completed')
    deadline_at = request.json.get('deadline_at')
    inserted_todo_id = database.insert_todo(title, description, completed, deadline_at)
    inserted_todo_object = database.get_todo_by_id(inserted_todo_id)
    return jsonify(inserted_todo_object), POST_RETURN_STATUS

@api.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id: int):
    title = request.json.get('title')
    description = request.json.get('description')
    completed = request.json.get('completed')
    deadline_at = request.json.get('deadline_at')
    database.update_todo(id, title, description, completed, deadline_at)

    updated_todo = database.get_todo_by_id(id)
    return jsonify(updated_todo)

@api.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id: int):
    object_to_delete = database.get_todo_by_id(id)
    database.delete_todo(id)
    return jsonify(object_to_delete)
