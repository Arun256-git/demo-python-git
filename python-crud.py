# First CRUD operation program in Python
from fastapi import FastAPI, HTTPException

from enum import IntEnum
from pydantic import BaseModel, Field
from typing import Optional, List

api = FastAPI()


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TodoBaseModel(BaseModel):
    priority: Priority = Field(description="Priority of task", default=Priority.LOW)
    todo_name: str = Field(..., max_length=100, min_length=1, description='Name of the task')
    todo_description: str = Field(..., description='Description of the task')


class TodoCreate(TodoBaseModel):
    pass


class Todo(TodoBaseModel):
    todo_id: int = Field(..., description='ID of the task')


class TodoUpdate(BaseModel):
    priority: Optional[Priority] = Field(None, description="Priority of task")
    todo_name: Optional[str] = Field(None, max_length=100, min_length=1, description='Name of the task')
    todo_description: Optional[str] = Field(None, description='Description of the task')


all_todos = [
    Todo(todo_id=1, priority=Priority.MEDIUM, todo_name="Todo1", todo_description="Todo1"),
    Todo(todo_id=2, priority=Priority.LOW, todo_name="Todo2", todo_description="Todo2"),
    Todo(todo_id=3, priority=Priority.HIGH, todo_name="Todo3", todo_description="Todo3"),
    Todo(todo_id=4, priority=Priority.LOW, todo_name="Todo4", todo_description="Todo4"),
]


# @api.get('/')
# def root():
#     return {'message': 'Hello World'}

@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail=' Todo not found')


@api.get('/todos', response_model= List[Todo])
def list_todos(first_n: int = None):
    if first_n is None:
        return all_todos
    else:
        return all_todos[:first_n]


@api.post('/todos', response_model= Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1

    new_todo= Todo(
        todo_id=new_todo_id,
        todo_name= todo.todo_name,
        todo_description=todo.todo_description,
        priority= todo.priority
    )

    all_todos.append(new_todo)
    return new_todo


@api.put('/todos/{todo_id}', response_model= Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if todo_update.todo_name is not None:
                todo.todo_name = todo_update.todo_name
            if todo_update.todo_description is not None:
                todo.todo_description = todo_update.todo_description
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')

@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            delete_todo = all_todos.pop(index)
            return delete_todo
    raise HTTPException(status_code=404, detail='Todo not found')
