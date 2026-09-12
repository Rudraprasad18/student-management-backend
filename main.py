import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

class StudentCreate(BaseModel):
    name: str
    branch: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL is working!"}


@app.get("/students")
def get_students():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, branch FROM students ORDER BY id;"
        )
        rows = cursor.fetchall()

    connection.close()

    students = [
        {
            "id": row[0],
            "name": row[1],
            "branch": row[2],
        }
        for row in rows
    ]

    return students


@app.post("/students")
def create_student(student: StudentCreate):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO students (name, branch)
            VALUES (%s, %s)
            RETURNING id, name, branch;
            """,
            (student.name, student.branch),
        )
        row = cursor.fetchone()

    connection.commit()
    connection.close()

    return {
        "id": row[0],
        "name": row[1],
        "branch": row[2],
    }

@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE students
            SET name = %s, branch = %s
            WHERE id = %s
            RETURNING id, name, branch;
            """,
            (student.name, student.branch, student_id),
        )
        row = cursor.fetchone()

    connection.commit()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return {
        "id": row[0],
        "name": row[1],
        "branch": row[2],
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM students
            WHERE id = %s
            RETURNING id, name, branch;
            """,
            (student_id,),
        )
        row = cursor.fetchone()

    connection.commit()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return {
        "message": "Student deleted successfully",
        "student": {
            "id": row[0],
            "name": row[1],
            "branch": row[2],
        },
    }