# First CRUD operation program in Python
from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def root():
    return {'message': 'Hello World'}