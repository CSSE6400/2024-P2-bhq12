from flask import Blueprint, jsonify, request, abort
from todo.models.todo import ToDoDatabaseHelper
api = Blueprint('api', __name__, url_prefix='/api/v1')

POST_RETURN_STATUS = 201
EXPECTED_POST_KEYS = ['title', 'description', 'completed', 'deadline_at']

@api.route('/health')
def health():
    return jsonify({'status': 'ok'})

@api.route('/todos', methods=['GET'])
def get_todos():
    completed_filter = None
    window_filter = None
    if 'completed' in request.args: 
        if request.args['completed'] == 'true':
            completed_filter = 1
        if request.args['completed'] == 'false':
            completed_filter = 0
    if 'window' in request.args:
        if request.args['window'].isdigit():
            window_filter = int(request.args['window'])
            
    database_helper = ToDoDatabaseHelper()
    return jsonify(database_helper.get_all_todos(completed_filter, window_filter))

@api.route('/todos/<int:id>', methods=['GET'])
def get_todo(id: int):
    database_helper = ToDoDatabaseHelper()
    todo_entry = database_helper.get_todo_by_id(id)
    if todo_entry is not None:
        return jsonify(todo_entry)
    else:
        abort(404)



@api.route('/todos', methods=['POST'])
def create_todo():

    database_helper = ToDoDatabaseHelper()
    for key in request.json.keys():
        if key not in EXPECTED_POST_KEYS:
            abort(400)
    for key in EXPECTED_POST_KEYS:
        if key not in request.json:
            abort(400)

    title = request.json.get('title')
    description = request.json.get('description')
    completed = request.json.get('completed')
    deadline_at = request.json.get('deadline_at')
    inserted_todo_id = database_helper.insert_todo(title, description, completed, deadline_at)
    inserted_todo_object = database_helper.get_todo_by_id(inserted_todo_id)
    return jsonify(inserted_todo_object), POST_RETURN_STATUS

@api.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id: int):
    database_helper = ToDoDatabaseHelper()

    for key in request.json.keys():
        if key not in ['title', 'description', 'completed', 'deadline_at']:
            abort(400)

    existing_todo = database_helper.get_todo_by_id(id)
    if existing_todo is None:
        abort(404)

    title = request.json.get('title')
    description = request.json.get('description')
    completed = request.json.get('completed')
    deadline_at = request.json.get('deadline_at')
    database_helper.update_todo(id, title, description, completed, deadline_at)

    updated_todo = database_helper.get_todo_by_id(id)
    return jsonify(updated_todo)

@api.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id: int):
    database_helper = ToDoDatabaseHelper()
    object_to_delete = database_helper.get_todo_by_id(id)
    database_helper.delete_todo(id)
    return jsonify(object_to_delete)
