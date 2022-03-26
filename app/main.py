from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import user, auth, select_courses

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='hackrushwebd', user='postgres', password='password123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as e:
        print(f'Could not connect to the database: \n[Error] {e}\nRetrying...')
        time.sleep(2)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(select_courses.router)

@app.get('/')
async def root():
    return {"detail": "Hello World!"}

