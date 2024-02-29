import os
import sqlite3
sqlite3.enable_callback_tracebacks(True)

SQLITE_DB_LOCATION = 'instance/db.sqlite'

SQL_FILES_LOCATION = 'todo/models/sql'

class ToDoDatabaseHelper():
    def __init__(self, db_location: str = SQLITE_DB_LOCATION, sql_files_location: str = SQL_FILES_LOCATION): 
        db_env_variable = os.getenv('SQLITE_DB_LOCATION')
        print(f'db_env: {db_env_variable}')
        self.db_location = db_env_variable if db_env_variable is not None else db_location
        self.sql_files_location = sql_files_location
        print(f'Instantiated ToDoDatabaseHelper for sqlite db: {self.db_location}')


    def dict_factory(self, cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    def instantiate_database_tables(self):
        connection = sqlite3.connect(self.db_location)
        connection.set_trace_callback(print)
        cursor = connection.cursor()
        create_table_sql = ''
        with open(f'{self.sql_files_location}/create_todo.sql') as file:
            create_table_sql = file.read()

        cursor.execute(create_table_sql)
        print('Instantiated tables')
        cursor.close()
        connection.close()


    ## HERE FOR UNIT TESTS AGAINST MEMORY DATABASE ONLY
    def _instantiate_database_tables_from_scratch_CAREFUL(self):
        connection = sqlite3.connect(self.db_location)
        connection.set_trace_callback(print)
        cursor = connection.cursor()
        table_sql = ''
        with open(f'{self.sql_files_location}/drop_table_todo.sql') as file:
            table_sql = file.read()

        cursor.execute(table_sql)

        table_sql = ''
        with open(f'{self.sql_files_location}/create_table_todo.sql') as file:
            table_sql = file.read()

        cursor.execute(table_sql)
        print('Instantiated tables')
        cursor.close()
        connection.close()



    def get_all_todos(self, completed_filter = None, window_filter = None):
        print('calling get_all_todos')
        connection = sqlite3.connect(self.db_location)
        connection.set_trace_callback(print)
        cursor = connection.cursor()

        get_todos_sql = ''
        with open(f'{self.sql_files_location}/get_all_todos.sql') as file:
            get_todos_sql = file.read()

        cursor.execute(get_todos_sql, (completed_filter, window_filter))
        result = []
        for row in cursor:
            result.append(self.dict_factory(cursor, row))
        cursor.close()
        connection.close()
        return result

    def insert_todo(self, title: str, description: str, completed: bool, deadline_at: str):
        connection = sqlite3.connect(self.db_location) 
        connection.set_trace_callback(print)
        cursor = connection.cursor()
        
        todo_sql = ''
        with open(f'{self.sql_files_location}/insert_todo.sql') as file:
            todo_sql = file.read()

        cursor.execute(todo_sql, (title, description, completed, deadline_at))

        new_todo_row_id = cursor.lastrowid
        cursor.close()
        connection.commit()
        connection.close()
        return new_todo_row_id

    def insert_todo_with_id(self, id: int, title: str, description: str, completed: bool, deadline_at: str):
        connection = sqlite3.connect(self.db_location) 
        connection.set_trace_callback(print)
        cursor = connection.cursor()
        
        todo_sql = ''
        with open(f'{self.sql_files_location}/insert_todo_with_id.sql') as file:
            todo_sql = file.read()

        cursor.execute(todo_sql, (id, title, description, completed, deadline_at))

        new_todo_row_id = id
        cursor.close()
        connection.commit()
        connection.close()
        return new_todo_row_id

    def update_todo(self, id: int, title: str, description: str, completed: bool, deadline_at: str):
        connection = sqlite3.connect(self.db_location) 
        connection.set_trace_callback(print)
        cursor = connection.cursor()
        
        todo_sql = ''
        with open(f'{self.sql_files_location}/update_todo.sql') as file:
            todo_sql = file.read()

        cursor.execute(todo_sql, (title, description, completed, deadline_at, id))
        cursor.close()
        connection.commit()
        connection.close()

    def delete_todo(self, id: int):
        connection = sqlite3.connect(self.db_location) 
        connection.set_trace_callback(print)
        cursor = connection.cursor()
        
        todo_sql = ''
        with open(f'{self.sql_files_location}/delete_todo.sql') as file:
            todo_sql = file.read()

        cursor.execute(todo_sql, (id,))
        cursor.close()
        connection.commit()
        connection.close()

    def get_todo_by_id(self, id: int):
        connection = sqlite3.connect(self.db_location)
        connection.set_trace_callback(print)
        cursor = connection.cursor()

        get_todo_sql = ''
        with open(f'{self.sql_files_location}/get_todo.sql') as file:
            get_todo_sql = file.read()

        cursor.execute(get_todo_sql, (id,))
        result = []
        for row in cursor:
            result.append(self.dict_factory(cursor, row))
        cursor.close()
        connection.close()

        if len(result) == 1:
            return result[0]
        else:
            return None
