from fastapi import APIRouter, HTTPException, status

from app.database.connection import get_connection
from app.schemas.student import StudentCreate

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("")
def get_students():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, branch FROM students ORDER BY id;"
        )
        rows = cursor.fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "branch": row[2],
        }
        for row in rows
    ]


@router.post("")
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


@router.put("/{student_id}")
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


@router.delete("/{student_id}")
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