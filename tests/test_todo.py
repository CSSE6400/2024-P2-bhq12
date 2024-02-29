from tests.base import TodoTest
from datetime import datetime, timedelta
from todo.models.todo import ToDoDatabaseHelper

TODO_1 = {
            "id": 1,
            "title": "Watch CSSE6400 Lecture",
            "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
            "completed": True,
            "deadline_at": "2023-02-27T00:00:00",
        }

TODO_2 = {
            "id": 2,
            "title": "Pass Practical Tests",
            "description": "Pass the practical tests for CSSE6400",
            "completed": False,
            "deadline_at": "2023-03-01T00:00:00",
        }

# a todo in 4 days time
TODO_FUTURE_1 = {
            "id": 3,
            "title": "Watch CSSE6400 Lecture 13",
            "description": "Watch the CSSE6400 lecture on ECHO360 for week 13",
            "completed": False,
            "deadline_at": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%dT00:00:00"),
        }

# a todo in 10 days time
TODO_FUTURE_2 = {
            "id": 4,
            "title": "Watch CSSE6400 Lecture 14",
            "description": "Watch the CSSE6400 lecture on ECHO360 for week 14",
            "completed": False,
            "deadline_at": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT00:00:00"),
        }


class TestTodo(TodoTest):
    def _populate_records(self, todos):
        # Instantiate tables if not exists
        database_helper = ToDoDatabaseHelper()

        for todo in todos:
            database_helper.insert_todo_with_id(todo['id'], todo['title'], todo['description'], todo['completed'], todo['deadline_at'])

    def _cleanup_todos(self, todos):
        print('instantiating db for _cleanup_todos')
        database_helper = ToDoDatabaseHelper()

        for todo in todos:
            database_helper.delete_todo(todo['id'])

    def test_get_item(self):
        todos = [TODO_1]
        self._populate_records(todos)

        response = self.client.get('/api/v1/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertDictSubset(TODO_1, response.json)

        self._cleanup_todos(todos)

    def test_get_item_multiple(self):
        todos = [TODO_1, TODO_2]
        self._populate_records(todos)

        response = self.client.get('/api/v1/todos/2')
        self.assertEqual(response.status_code, 200)
        self.assertDictSubset(TODO_2, response.json)
        self._cleanup_todos(todos)

    def test_get_todo_not_found(self):
        response = self.client.get('/api/v1/todos/1')
        self.assertEqual(response.status_code, 404)
 
    def test_get_items_empty(self):
        response = self.client.get('/api/v1/todos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_items(self):
        todos = [TODO_1, TODO_2]
        self._populate_records(todos)

        response = self.client.get('/api/v1/todos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertDictSubset(TODO_1, response.json[0])
        self.assertDictSubset(TODO_2, response.json[1])
        self._cleanup_todos(todos)

    def test_get_items_completed(self):
        todos = [TODO_1, TODO_2]
        self._populate_records(todos)

        response = self.client.get('/api/v1/todos?completed=true')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertDictSubset(TODO_1, response.json[0])
        self._cleanup_todos(todos)

    def test_get_items_window(self):
        todos = [TODO_1, TODO_2, TODO_FUTURE_1, TODO_FUTURE_2]
        self._populate_records(todos)

        response = self.client.get('/api/v1/todos?window=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertDictSubset(TODO_1, response.json[0])
        self.assertDictSubset(TODO_2, response.json[1])
        self.assertDictSubset(TODO_FUTURE_1, response.json[2])
        self._cleanup_todos(todos)

    def test_post_item_success(self):
        todo = TODO_1.copy()
        del todo['id']

        response = self.client.post('/api/v1/todos', json=todo)
        self.assertEqual(response.status_code, 201)
        self.assertDictSubset(TODO_1, response.json)

    def test_post_item_missing_title(self):
        todo = TODO_1.copy()
        del todo['id']
        del todo['title']
        response = self.client.post('/api/v1/todos', json=todo)
        self.assertEqual(response.status_code, 400)

        
    def test_post_item_extra_field(self):
        todo = TODO_1.copy()
        todo['extra'] = 'extra'
        response = self.client.post('/api/v1/todos', json=todo)
        self.assertEqual(response.status_code, 400)

    def test_post_item_success_then_get(self):
        todo = TODO_1.copy()
        del todo['id']
        response = self.client.post('/api/v1/todos', json=todo)
        self.assertEqual(response.status_code, 201)
        self.assertDictSubset(TODO_1, response.json)

        response = self.client.get('/api/v1/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertDictSubset(TODO_1, response.json)

    def test_post_item_defaults(self):
        todo = TODO_1.copy()
        del todo['completed']
        del todo['deadline_at']
        del todo['id']
        response = self.client.post('/api/v1/todos', json=todo)
        self.assertEqual(response.status_code, 201)
        self.assertDictSubset(todo, response.json)
        self.assertFalse(response.json['completed'])
        self.assertIsNone(response.json['deadline_at'])

    def test_put_item_success(self):
        todos = [TODO_1]
        self._populate_records(todos)

        todo = {"title": "New Title"}
        response = self.client.put('/api/v1/todos/1', json=todo)
        self.assertEqual(response.status_code, 200)
        self.assertDictSubset(todo, response.json)
        self._cleanup_todos(todos)

    def test_put_item_extra_field(self):
        todos = [TODO_1]
        self._populate_records(todos)

        todo = {"extra": "extra"}
        response = self.client.put('/api/v1/todos/1', json=todo)
        self.assertEqual(response.status_code, 400)
        self._cleanup_todos(todos)

    def test_put_item_not_found(self):
        todo = {"title": "New Title"}
        response = self.client.put('/api/v1/todos/1', json=todo)
        self.assertEqual(response.status_code, 404)

    def test_put_item_change_id(self):
        todos = [TODO_1]
        self._populate_records(todos)

        todo = {"id": 2}
        response = self.client.put('/api/v1/todos/1', json=todo)
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/api/v1/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertDictSubset(TODO_1, response.json)
        self._cleanup_todos(todos)

    def test_put_item_success_then_get(self):
        todos = [TODO_1]
        self._populate_records(todos)

        todo = {"title": "New Title"}
        response = self.client.put('/api/v1/todos/1', json=todo)
        self.assertEqual(response.status_code, 200)
        self.assertDictSubset(todo, response.json)

        response = self.client.get('/api/v1/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertDictSubset(todo, response.json)
        self._cleanup_todos(todos)

    def test_delete_item_success(self):
        todos = [TODO_1]
        self._populate_records(todos)

        response = self.client.delete('/api/v1/todos/1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/todos/1')
        self.assertEqual(response.status_code, 404)
        self._cleanup_todos(todos)

    def test_delete_item_not_found(self):
        response = self.client.delete('/api/v1/todos/1')
        self.assertEqual(response.status_code, 200)
